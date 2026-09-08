"""Build the training file with one column per source and isoform, instead of one pooled column.

Pooling calibrated sources dragged the scored target down to the qHTS spread (~0.6) when the
challenge assay's own spread is ~1.0; keeping sources in their own columns lets each become its
own prediction head, so the scored head trains only on challenge-scale values.

Usage:
    python examples/cyp_challenge/scripts/build_multisource_dataset.py
"""

import argparse
import os

import numpy as np
import pandas as pd
from datasets import load_dataset
from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(CHALLENGE_DIR, "data", "raw")
OUT_PATH = os.path.join(CHALLENGE_DIR, "data", "processed", "multisource_pac50.csv")
CHALLENGE_DATASET = "openadmet/cyp-challenge-train-test"

ENDPOINTS = ["cyp1a2", "cyp2c9", "cyp2d6", "cyp3a4"]

QHTS_FITTED = ["veith.csv", "ncgc.csv"]
# every value in this file is an upper bound (4.244), never a measurement
QHTS_CENSORED = "aid1851_inactives.csv"
PUBLIC_SOURCES = {
    "pharmabench": ["pharmabench.csv"],
    "tox21": ["tox21_luciferase_kept.csv"],
}

# OpenADMET's curated ChEMBL-37 panel, one parquet per isoform, pchembl_value_mean as the label
CHEMBL_FILES = {
    "cyp1a2": "chembl_CYP1A2_CHEMBL3356.parquet",
    "cyp2c9": "chembl_CYP2C9_CHEMBL3397.parquet",
    "cyp2d6": "chembl_CYP2D6_CHEMBL289.parquet",
    "cyp3a4": "chembl_CYP3A4_CHEMBL340.parquet",
}
# Octant's own CYP3A4 release: the challenge assay, run by the challenge lab
OCTANT_FILE = "octant_cyp3a4.tsv"


def canonical(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(mol) if mol is not None else None


def value_column(frame, endpoint):
    """Source files use either pac50_<endpoint> or pic50_<endpoint>."""
    for prefix in ("pac50_", "pic50_"):
        if prefix + endpoint in frame.columns:
            return prefix + endpoint
    return None


def read_source(paths, raw_dir):
    """Canonicalise and average the given files into one frame of SMILES + per-endpoint values."""
    frames = []
    for name in paths:
        frame = pd.read_csv(os.path.join(raw_dir, name))
        if "luciferase_artifact" in frame.columns:
            # luciferase inhibitors read as CYP inhibitors in this luminogenic assay
            frame = frame[~frame.luciferase_artifact.astype(bool)]
        frame["SMILES"] = [canonical(s) for s in frame.SMILES]
        frame = frame.dropna(subset=["SMILES"])
        keep = {"SMILES": frame.SMILES}
        for endpoint in ENDPOINTS:
            column = value_column(frame, endpoint)
            keep[endpoint] = pd.to_numeric(frame[column], errors="coerce") if column else np.nan
        frames.append(pd.DataFrame(keep))
    return pd.concat(frames, ignore_index=True).groupby("SMILES", as_index=False).mean()


def read_challenge():
    train = load_dataset(CHALLENGE_DATASET)["train"].to_pandas()
    train["SMILES"] = [canonical(s) for s in train.SMILES]
    train = train.dropna(subset=["SMILES"])
    keep = {"SMILES": train.SMILES}
    for endpoint in ENDPOINTS:
        keep[endpoint] = pd.to_numeric(
            train[f"{endpoint.upper()}_pIC50_direct_inhibition"], errors="coerce")
    return pd.DataFrame(keep).groupby("SMILES", as_index=False).mean()


def build_qhts(raw_dir):
    """The qHTS group: fitted values from every export, plus AID 1851's inactives as bounds.

    An inactive only says "at most this potent", so a fitted measurement from any export always
    wins over AID 1851's censored bound for the same compound.
    """
    fitted = read_source(QHTS_FITTED, raw_dir).set_index("SMILES")

    bounds = pd.read_csv(os.path.join(raw_dir, QHTS_CENSORED))
    bounds["SMILES"] = [canonical(s) for s in bounds.SMILES]
    bounds = bounds.dropna(subset=["SMILES"]).drop_duplicates("SMILES").set_index("SMILES")

    index = sorted(set(fitted.index) | set(bounds.index))
    out = pd.DataFrame({"SMILES": index}).set_index("SMILES")
    for endpoint in ENDPOINTS:
        bound = bounds.get(f"pac50_{endpoint}", pd.Series(dtype=float)).reindex(index)
        observed = fitted[endpoint].reindex(index) if endpoint in fitted else pd.Series(np.nan, index)

        out[endpoint] = observed.where(observed.notna(), bound)
        out[f"{endpoint}__lt"] = observed.isna() & bound.notna()
    return out.reset_index()


def read_chembl(raw_dir):
    """One column per isoform from OpenADMET's ChEMBL-37 aggregation."""
    frames = []
    for endpoint, name in CHEMBL_FILES.items():
        path = os.path.join(raw_dir, "chembl", name)
        if not os.path.exists(path):
            continue
        frame = pd.read_parquet(path)
        keep = pd.DataFrame({
            "SMILES": [canonical(s) for s in frame.OPENADMET_CANONICAL_SMILES],
            endpoint: pd.to_numeric(frame.pchembl_value_mean, errors="coerce"),
        }).dropna(subset=["SMILES"])
        frames.append(keep.groupby("SMILES", as_index=False).mean())

    merged = None
    for frame in frames:
        merged = frame if merged is None else merged.merge(frame, on="SMILES", how="outer")
    return merged if merged is not None else pd.DataFrame({"SMILES": []})


def read_octant(raw_dir):
    """Octant's CYP3A4 release, restricted to curves that passed their own QC."""
    path = os.path.join(raw_dir, OCTANT_FILE)
    if not os.path.exists(path):
        return pd.DataFrame({"SMILES": []})
    frame = pd.read_csv(path, sep="\t")
    frame = frame[frame.drc_qc_status.eq("PASS")]
    keep = pd.DataFrame({
        "SMILES": [canonical(s) for s in frame.standardized_smiles],
        "cyp3a4": pd.to_numeric(frame.CYP3A4_pIC50, errors="coerce"),
    }).dropna(subset=["SMILES"])
    return keep.groupby("SMILES", as_index=False).mean()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", default=RAW_DIR)
    parser.add_argument("--out", default=OUT_PATH)
    parser.add_argument("--no-censored", action="store_true",
                        help="skip AID 1851's censored inactives, keeping only fitted values")
    parser.add_argument("--extra", action="store_true",
                        help="add ChEMBL-37 and Octant's CYP3A4 release as their own heads")
    args = parser.parse_args()

    if args.no_censored:
        groups = {"challenge": read_challenge(),
                  "qhts": read_source(QHTS_FITTED, args.raw_dir)}
    else:
        groups = {"challenge": read_challenge(),
                  "qhts": build_qhts(args.raw_dir)}
    for name, paths in PUBLIC_SOURCES.items():
        groups[name] = read_source(paths, args.raw_dir)
    if args.extra:
        groups["chembl"] = read_chembl(args.raw_dir)
        groups["octant"] = read_octant(args.raw_dir)

    merged = None
    for name, frame in groups.items():
        renames = {e: f"{name}_{e}" for e in ENDPOINTS}
        renames.update({f"{e}__lt": f"{name}_{e}__lt" for e in ENDPOINTS})
        frame = frame.rename(columns=renames)
        merged = frame if merged is None else merged.merge(frame, on="SMILES", how="outer")

    # PharmaBench has no CYP1A2, so some columns come out empty
    targets = [c for c in merged.columns
               if c != "SMILES" and not c.endswith("__lt") and merged[c].notna().any()]
    flags = [f"{c}__lt" for c in targets if f"{c}__lt" in merged.columns]
    merged = merged[["SMILES"] + targets + flags]
    merged = merged[merged[targets].notna().any(axis=1)].reset_index(drop=True)
    for flag in flags:
        merged[flag] = merged[flag] == True  # noqa: E712 - NaN must become False, not NaN

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    merged.to_csv(args.out, index=False)

    print(f"{len(merged)} compounds, {len(targets)} target columns "
          f"({merged[targets].notna().to_numpy().mean():.1%} label density)\n")
    print(f"  {'column':26} {'n':>7} {'mean':>8} {'sd':>8} {'censored':>9}")
    for column in targets:
        values = merged[column].dropna()
        flag = f"{column}__lt"
        n_censored = int((merged[flag] & merged[column].notna()).sum()) if flag in merged else 0
        marker = "  <- scored" if column.startswith("challenge_") else ""
        print(f"  {column:26} {len(values):7d} {values.mean():8.3f} {values.std():8.3f}"
              f" {n_censored:9d}{marker}")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
