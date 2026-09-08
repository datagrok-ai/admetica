"""Put every CYP source on the OpenADMET pIC50 scale, then rebuild the training sets.

Per-source offsets are fitted jointly by least squares (`value(i, j) = potency(i) + offset(j)`)
with the challenge source anchored at 0; calibrated targets are `value - offset(source)`.

Usage:
    python examples/cyp_challenge/scripts/calibrate_cyp_sources.py
"""

import os

import numpy as np
import pandas as pd
from datasets import load_dataset
from rdkit import Chem, RDLogger
from scipy.sparse import coo_matrix, csr_matrix, vstack
from scipy.sparse.linalg import lsqr
from tabulate import tabulate

RDLogger.DisableLog("rdApp.*")
pd.set_option("future.no_silent_downcasting", True)

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(os.path.dirname(CHALLENGE_DIR))
OUT_DIR = os.path.join(CHALLENGE_DIR, "data")

RAW_DIR = os.path.expanduser("~/Downloads")
RAW_FILES = {
    "tox21": "train_tox21_luciferase_removed (1).csv",
    "pharmabench": "train_pharmabench.csv",
    "veith": "train_veith.csv",
    "ncgc": "train_ncgc.csv",
}
CHALLENGE_DATASET = "openadmet/cyp-challenge-train-test"
REFERENCE_SOURCE = "challenge"          # the scale everything is aligned to

ENDPOINTS = ["cyp1a2", "cyp2c9", "cyp2d6", "cyp3a4"]
ANCHOR_WEIGHT = 100.0                   # weight on the offset(reference) = 0 constraint


def canon(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(mol) if mol is not None else None


def target_column(source_name, endpoint):
    if source_name == "challenge":
        return f"{endpoint.upper()}_pIC50_direct_inhibition"
    if source_name == "pharmabench":
        return f"pic50_{endpoint}"
    return f"pac50_{endpoint}"


def load_sources():
    sources = {}
    challenge = load_dataset(CHALLENGE_DATASET)["train"].to_pandas()
    challenge["can"] = [canon(s) for s in challenge.SMILES]
    sources["challenge"] = challenge.dropna(subset=["can"])
    for name, filename in RAW_FILES.items():
        df = pd.read_csv(os.path.join(RAW_DIR, filename))
        df["can"] = [canon(s) for s in df.SMILES]
        sources[name] = df.dropna(subset=["can"])
    return sources


def measurements_for(endpoint, sources):
    """One row per (compound, source) measurement, deduplicated within each source."""
    frames = []
    for name, df in sources.items():
        column = target_column(name, endpoint)
        if column not in df.columns:
            continue
        keep = df[column].notna()
        if name == "pharmabench":
            keep = keep & ~df[f"censored_{endpoint}"].fillna(False).astype(bool)
        series = df.loc[keep].groupby("can")[column].mean()
        frames.append(series.rename("y").reset_index().assign(source=name))
    return pd.concat(frames, ignore_index=True)


def fit_offsets(measurements):
    """Least-squares offsets per source, anchored so the reference source sits at zero."""
    counts = measurements.groupby("can").size()
    shared = measurements[measurements.can.isin(counts[counts >= 2].index)]

    compounds = {c: i for i, c in enumerate(shared.can.unique())}
    source_names = list(shared.source.unique())
    source_index = {s: i for i, s in enumerate(source_names)}
    n_compounds, n_sources = len(compounds), len(source_names)

    rows = np.arange(len(shared))
    design = coo_matrix(
        (np.ones(2 * len(shared)),
         (np.concatenate([rows, rows]),
          np.concatenate([shared.can.map(compounds).values,
                          n_compounds + shared.source.map(source_index).values]))),
        shape=(len(shared), n_compounds + n_sources),
    )

    anchor = np.zeros((1, n_compounds + n_sources))
    anchor[0, n_compounds + source_index[REFERENCE_SOURCE]] = ANCHOR_WEIGHT
    solution = lsqr(vstack([design, csr_matrix(anchor)]),
                    np.concatenate([shared.y.values, [0.0]]),
                    atol=1e-10, btol=1e-10, iter_lim=20000)[0]

    offsets = {s: float(solution[n_compounds + source_index[s]]) for s in source_names}
    support = shared.groupby("source").size().to_dict()
    return offsets, support, len(compounds)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sources = load_sources()

    offset_rows, summary_rows = [], []

    for endpoint in ENDPOINTS:
        measurements = measurements_for(endpoint, sources)
        offsets, support, n_shared = fit_offsets(measurements)

        for name, offset in sorted(offsets.items()):
            offset_rows.append({
                "endpoint": endpoint, "source": name, "offset": round(offset, 4),
                "measurements_in_fit": support.get(name, 0),
            })

        calibrated = measurements.copy()
        calibrated["y"] = calibrated.y - calibrated.source.map(offsets)

        merged = calibrated.groupby("can").agg(
            pAC50=("y", "mean"),
            source=("source", lambda s: ";".join(sorted(set(s)))),
        ).reset_index().rename(columns={"can": "SMILES"})

        merged.to_csv(os.path.join(OUT_DIR, f"{endpoint}_pac50.csv"), index=False)

        raw_merged = measurements.groupby("can").y.mean()
        summary_rows.append({
            "endpoint": endpoint,
            "compounds": len(merged),
            "shared_compounds_in_fit": n_shared,
            "mean_before": round(raw_merged.mean(), 3),
            "mean_after": round(merged.pAC50.mean(), 3),
            "std_after": round(merged.pAC50.std(), 3),
        })
        print(f"{endpoint}: {len(merged)} compounds written")

    pd.DataFrame(offset_rows).to_csv(os.path.join(OUT_DIR, "source_offsets.csv"), index=False)

    print("\nFitted offsets (log units above the OpenADMET scale)\n")
    table = pd.DataFrame(offset_rows).pivot(index="source", columns="endpoint", values="offset")
    print(tabulate(table, headers="keys", tablefmt="github"))
    print("\n" + tabulate(pd.DataFrame(summary_rows), headers="keys",
                          tablefmt="github", showindex=False))
    print(f"\nwrote {OUT_DIR}")


if __name__ == "__main__":
    main()
