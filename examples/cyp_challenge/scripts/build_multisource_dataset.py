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

# Veith and NCGC are two extractions of one campaign (rho 0.99, mean abs difference 0.006), so they
# are averaged into a single qHTS group rather than counted as independent evidence.
PUBLIC_SOURCES = {
    "qhts": ["veith.csv", "ncgc.csv"],
    "pharmabench": ["pharmabench.csv"],
    "tox21": ["tox21_luciferase_kept.csv"],
}


def canonical(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(mol) if mol is not None else None


def value_column(frame, endpoint):
    """Source files use pac50_<endpoint> or pic50_<endpoint>; return whichever exists."""
    for prefix in ("pac50_", "pic50_"):
        if prefix + endpoint in frame.columns:
            return prefix + endpoint
    return None


def read_source(paths, raw_dir):
    """Canonicalise and average the given files into one frame of SMILES + per-endpoint values."""
    frames = []
    for name in paths:
        frame = pd.read_csv(os.path.join(raw_dir, name))
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", default=RAW_DIR)
    parser.add_argument("--out", default=OUT_PATH)
    args = parser.parse_args()

    groups = {"challenge": read_challenge()}
    for name, paths in PUBLIC_SOURCES.items():
        groups[name] = read_source(paths, args.raw_dir)

    merged = None
    for name, frame in groups.items():
        frame = frame.rename(columns={e: f"{name}_{e}" for e in ENDPOINTS})
        merged = frame if merged is None else merged.merge(frame, on="SMILES", how="outer")

    # drop all-empty columns (PharmaBench has no CYP1A2) and rows with no measurement at all
    targets = [c for c in merged.columns if c != "SMILES" and merged[c].notna().any()]
    merged = merged[["SMILES"] + targets]
    merged = merged[merged[targets].notna().any(axis=1)].reset_index(drop=True)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    merged.to_csv(args.out, index=False)

    print(f"{len(merged)} compounds, {len(targets)} target columns "
          f"({merged[targets].notna().to_numpy().mean():.1%} label density)\n")
    print(f"  {'column':26} {'n':>7} {'mean':>8} {'sd':>8}")
    for column in targets:
        values = merged[column].dropna()
        marker = "  <- scored" if column.startswith("challenge_") else ""
        print(f"  {column:26} {len(values):7d} {values.mean():8.3f} {values.std():8.3f}{marker}")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
