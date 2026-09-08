"""Combine the trained members into one submission.

Weights are fitted per endpoint on the out-of-fold predictions the members share, by grid search
over the challenge metric rather than least squares, because the metric is what decides the
leaderboard. Placement (centre and spread) is fitted the same way, on the weighted blend.

Members are declared in MEMBERS: each needs out-of-fold predictions for weight fitting, and a
production checkpoint to predict the blinded test set.

Usage:
    python examples/cyp_challenge/scripts/build_ensemble_submission.py
    python examples/cyp_challenge/scripts/build_ensemble_submission.py --members champion,e3a
"""

import argparse
import glob
import itertools
import logging
import os
import warnings

logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from datasets import load_dataset
from lightning import pytorch as pl
from rdkit import Chem, RDLogger
from chemprop import data, featurizers, models

RDLogger.DisableLog("rdApp.*")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, "results")
TEST_URL = "hf://datasets/openadmet/cyp-challenge-train-test/cyp-challenge-TEST-BLINDED.csv"
CHALLENGE_DATASET = "openadmet/cyp-challenge-train-test"

ENDPOINTS = ["cyp1a2", "cyp2c9", "cyp2d6", "cyp3a4"]
CYPS = [e.upper() for e in ENDPOINTS]
VALUE_COLUMNS = [f"{c}_pIC50_direct_inhibition" for c in CYPS]
SUBMISSION_COLUMNS = ["SMILES", "Molecule_Name"] + VALUE_COLUMNS
EXPECTED_ROWS = 750

# name -> (out-of-fold directory, production checkpoint, scored-head column indices)
MEMBERS = {
    "champion": (os.path.join(RESULTS, "chemeleon_multitask"),
                 os.path.join(BASE, "models", "multitask_pac50.ckpt"), [0, 1, 2, 3]),
    "e3a": (os.path.join(RESULTS, "multihead_nocensored"),
            os.path.join(RESULTS, "multihead_nocensored", "models", "multitask_pac50.ckpt"),
            [0, 1, 2, 3]),
    "e3b": (os.path.join(RESULTS, "multihead_censored"),
            os.path.join(RESULTS, "multihead_censored", "models", "multitask_pac50.ckpt"),
            [0, 1, 2, 3]),
    "chembl": (os.path.join(RESULTS, "chembl_octant"),
               os.path.join(RESULTS, "chembl_octant", "models", "multitask_pac50.ckpt"),
               [0, 1, 2, 3]),
    "e3a_v2": (os.path.join(RESULTS, "multihead_nocensored_v2"),
               os.path.join(RESULTS, "multihead_nocensored_v2", "models", "multitask_pac50.ckpt"),
               [0, 1, 2, 3]),
}

WEIGHT_STEP = 0.1          # grid resolution for the per-endpoint member weights
CENTRE_GRID = np.arange(-0.4, 0.41, 0.02)   # offset applied after blending
SPREAD_GRID = np.arange(0.7, 1.35, 0.05)    # multiplier on the blend's own spread


def rae(y, p, lo, hi):
    y, p, lo, hi = map(np.asarray, (y, p, lo, hi))
    error = np.clip(p - hi, 0, None) + np.clip(lo - p, 0, None)
    mean = y.mean()
    baseline = np.clip(mean - hi, 0, None) + np.clip(lo - mean, 0, None)
    return float(error.sum() / baseline.sum())


def canon(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(mol) if mol is not None else None


def load_oof(directory, endpoint):
    files = sorted(glob.glob(os.path.join(directory, f"oof_{endpoint}_fold*.csv")))
    if not files:
        return None
    frame = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    return frame.drop_duplicates("SMILES")[["SMILES", "observed", "predicted"]]


def weight_grid(n_members):
    """All simplex points on a WEIGHT_STEP grid, so weights are non-negative and sum to one."""
    steps = int(round(1 / WEIGHT_STEP))
    for counts in itertools.product(range(steps + 1), repeat=n_members):
        if sum(counts) == steps:
            yield np.array(counts, dtype=float) / steps


def fit_endpoint(endpoint, members, bounds):
    """Weights and placement for one endpoint, chosen on out-of-fold predictions."""
    frames = {}
    for name in members:
        oof = load_oof(MEMBERS[name][0], endpoint)
        if oof is not None:
            frames[name] = oof.set_index("SMILES")
    if not frames:
        return None

    shared = set.intersection(*(set(f.index) for f in frames.values()))
    shared &= set(bounds.index)
    shared = sorted(shared)
    if len(shared) < 100:
        return None

    label = f"{endpoint.upper()}_pIC50_direct_inhibition"
    observed = frames[list(frames)[0]].loc[shared, "observed"].to_numpy()
    low = bounds.loc[shared, f"{label}_conf_low"].to_numpy()
    high = bounds.loc[shared, f"{label}_conf_high"].to_numpy()
    keep = ~np.isnan(low) & ~np.isnan(high)
    observed, low, high = observed[keep], low[keep], high[keep]
    stack = np.column_stack([frames[n].loc[shared, "predicted"].to_numpy()[keep] for n in frames])

    names = list(frames)
    best = (np.inf, None, 0.0, 1.0)
    for weights in weight_grid(len(names)):
        blended = stack @ weights
        centre = blended.mean()
        for spread in SPREAD_GRID:
            scaled = (blended - centre) * spread + centre
            for offset in CENTRE_GRID:
                score = rae(observed, scaled + offset, low, high)
                if score < best[0]:
                    best = (score, weights, float(offset), float(spread))

    raw = {n: rae(observed, frames[n].loc[shared, "predicted"].to_numpy()[keep], low, high)
           for n in names}
    return {"endpoint": endpoint, "members": names, "weights": best[1], "rae": best[0],
            "offset": best[2], "spread": best[3], "n": int(keep.sum()), "per_member": raw}


def predict(checkpoint, smiles, columns):
    model = models.MPNN.load_from_checkpoint(checkpoint, map_location="cpu")
    points = [data.MoleculeDatapoint.from_smi(s) for s in smiles]
    loader = data.build_dataloader(
        data.MoleculeDataset(points, featurizers.SimpleMoleculeMolGraphFeaturizer()),
        num_workers=0, shuffle=False)
    trainer = pl.Trainer(logger=False, enable_progress_bar=False, accelerator="cpu", devices=1)
    return np.concatenate(trainer.predict(model, loader))[:, columns]


def validate(submission):
    errors = []
    if list(submission.columns) != SUBMISSION_COLUMNS:
        errors.append(f"columns are {list(submission.columns)}")
    if len(submission) != EXPECTED_ROWS:
        errors.append(f"{len(submission)} rows, expected {EXPECTED_ROWS}")
    if submission[["SMILES", "Molecule_Name"]].isna().any().any():
        errors.append("missing identifiers")
    if submission.Molecule_Name.duplicated().any():
        errors.append("duplicated Molecule_Name")
    for column in VALUE_COLUMNS:
        values = pd.to_numeric(submission[column], errors="coerce")
        if values.isna().any() or not np.isfinite(values.to_numpy()).all():
            errors.append(f"{column}: non-numeric, missing or infinite values")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--members", default=None,
                        help="comma-separated subset of " + ",".join(MEMBERS))
    parser.add_argument("--out", default=os.path.join(BASE, "cyp_challenge_submission_ensemble.csv"))
    args = parser.parse_args()

    wanted = args.members.split(",") if args.members else list(MEMBERS)
    available = [n for n in wanted
                 if os.path.exists(MEMBERS[n][1]) and glob.glob(os.path.join(MEMBERS[n][0], "oof_*.csv"))]
    missing = sorted(set(wanted) - set(available))
    if missing:
        print(f"skipping members without a checkpoint or out-of-fold predictions: {missing}")
    if not available:
        raise SystemExit("no usable members")
    print(f"members: {available}\n")

    train = load_dataset(CHALLENGE_DATASET)["train"].to_pandas()
    train["can"] = [canon(s) for s in train.SMILES]
    bounds = train.dropna(subset=["can"]).drop_duplicates("can").set_index("can")

    fits = {}
    for endpoint in ENDPOINTS:
        fit = fit_endpoint(endpoint, available, bounds)
        if fit is None:
            raise SystemExit(f"{endpoint}: not enough shared out-of-fold predictions")
        fits[endpoint] = fit
        weights = ", ".join(f"{n}={w:.1f}" for n, w in zip(fit["members"], fit["weights"]) if w > 0)
        print(f"{endpoint}: n={fit['n']:4d} RAE={fit['rae']:.4f} "
              f"(offset {fit['offset']:+.2f}, spread x{fit['spread']:.2f}) [{weights}]")
        print("          per member: "
              + ", ".join(f"{n}={v:.4f}" for n, v in fit["per_member"].items()))
    print(f"\nmacro out-of-fold RAE: {np.mean([f['rae'] for f in fits.values()]):.4f}")

    test = pd.read_csv(TEST_URL)
    parsed = [Chem.MolFromSmiles(s) for s in test.SMILES]
    if any(m is None for m in parsed):
        raise SystemExit("unparseable SMILES in the test set")
    canonical = [Chem.MolToSmiles(m) for m in parsed]

    predictions = {}
    for name in available:
        _, checkpoint, columns = MEMBERS[name]
        predictions[name] = predict(checkpoint, canonical, columns)
        print(f"predicted {len(test)} test molecules with {name}")

    submission = test[["SMILES", "Molecule_Name"]].copy()
    for index, endpoint in enumerate(ENDPOINTS):
        fit = fits[endpoint]
        stack = np.column_stack([predictions[n][:, index] for n in fit["members"]])
        blended = stack @ fit["weights"]
        centre = blended.mean()
        placed = (blended - centre) * fit["spread"] + centre + fit["offset"]
        submission[f"{endpoint.upper()}_pIC50_direct_inhibition"] = placed

    submission = submission[SUBMISSION_COLUMNS]
    errors = validate(submission)
    if errors:
        raise SystemExit("INVALID:\n" + "\n".join(errors))
    submission.to_csv(args.out, index=False)

    summary = pd.DataFrame([
        {"endpoint": e.upper(), "n_oof": f["n"], "oof_RAE": round(f["rae"], 4),
         "offset": f["offset"], "spread": f["spread"],
         **{f"w_{n}": round(w, 2) for n, w in zip(f["members"], f["weights"])}}
        for e, f in fits.items()])
    summary.to_csv(os.path.join(RESULTS, "ensemble_weights.csv"), index=False)
    print(f"\nwrote {args.out} ({len(submission)} rows) and results/ensemble_weights.csv")
    print(submission[VALUE_COLUMNS].describe().loc[["mean", "std", "min", "max"]].round(3))


if __name__ == "__main__":
    main()
