"""Install the CYP pAC50 regression datasets into the ADMET repository layout.

Writes `ADMET/metabolism/<endpoint>-inhibitor-pac50/` using the repository's `Drug`/`Y` column
convention, plus a `source` column; unlike the existing binary `cyp*-inhibitor` sets derived from
PubChem AID 1851, these hold continuous pAC50 values.

Usage:
    python examples/cyp_challenge/scripts/install_cyp_pac50_datasets.py
    python examples/cyp_challenge/scripts/install_cyp_pac50_datasets.py --checkpoints
"""

import argparse
import os
import shutil

import pandas as pd
from datasets import load_dataset
from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")
pd.set_option("future.no_silent_downcasting", True)

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(os.path.dirname(CHALLENGE_DIR))
METABOLISM_DIR = os.path.join(REPO_ROOT, "ADMET", "metabolism")
WORKING_DIR = os.path.join(CHALLENGE_DIR, "data")

RAW_DIR = os.path.expanduser("~/Downloads")
RAW_FILES = {
    "tox21": "train_tox21_luciferase_removed (1).csv",
    "pharmabench": "train_pharmabench.csv",
    "veith": "train_veith.csv",
    "ncgc": "train_ncgc.csv",
}

# In-domain source: the OpenADMET CYP challenge train split (the test split is blinded)
CHALLENGE_DATASET = "openadmet/cyp-challenge-train-test"

ENDPOINTS = ["cyp1a2", "cyp2c9", "cyp2d6", "cyp3a4"]


def dataset_name(endpoint):
    return f"{endpoint}-inhibitor-pac50"


def target_column(source_name, endpoint):
    """Each source names its target column differently, and not all are on the same scale."""
    if source_name == "challenge":
        return f"{endpoint.upper()}_pIC50_direct_inhibition"
    if source_name == "pharmabench":
        return f"pic50_{endpoint}"
    return f"pac50_{endpoint}"


def build_raw_union(endpoint, sources):
    """One row per source measurement, original SMILES, before canonicalization or merging."""
    frames = []
    for name, df in sources.items():
        col = target_column(name, endpoint)
        if col not in df.columns:
            continue

        keep = df[col].notna()
        if name == "pharmabench":
            keep = keep & ~df[f"censored_{endpoint}"].fillna(False).astype(bool)

        sub = df.loc[keep, ["SMILES", col]]
        sub.columns = ["Drug", "Y"]
        sub["source"] = name
        frames.append(sub)

    return pd.concat(frames, ignore_index=True)


def load_curated(endpoint):
    """The model-ready file produced by calibrate_cyp_sources.py."""
    path = os.path.join(WORKING_DIR, f"{endpoint}_pac50.csv")
    if not os.path.exists(path):
        raise SystemExit(
            f"Missing {path}. Run the preprocessing section of "
            f"calibrate_cyp_sources.py first."
        )
    curated = pd.read_csv(path).rename(columns={"SMILES": "Drug", "pAC50": "Y"})
    return curated[["Drug", "Y", "source"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoints",
        action="store_true",
        help="also copy trained .ckpt files from examples/cyp_training_data/models",
    )
    args = parser.parse_args()

    missing = [f for f in RAW_FILES.values() if not os.path.exists(os.path.join(RAW_DIR, f))]
    if missing:
        raise SystemExit(f"Raw source files not found in {RAW_DIR}: {missing}")

    sources = {
        name: pd.read_csv(os.path.join(RAW_DIR, filename))
        for name, filename in RAW_FILES.items()
    }
    sources["challenge"] = load_dataset(CHALLENGE_DATASET)["train"].to_pandas()

    for endpoint in ENDPOINTS:
        name = dataset_name(endpoint)
        target_dir = os.path.join(METABOLISM_DIR, name)
        os.makedirs(target_dir, exist_ok=True)

        raw = build_raw_union(endpoint, sources)
        raw.to_csv(os.path.join(target_dir, f"{name}.csv"), index=False)

        curated = load_curated(endpoint)
        curated.to_csv(os.path.join(target_dir, f"{name}_curated.csv"), index=False)

        line = f"{name}: {len(raw)} raw measurements -> {len(curated)} curated compounds"

        if args.checkpoints:
            checkpoint = os.path.join(WORKING_DIR, "models", f"{endpoint}_pac50.ckpt")
            if os.path.exists(checkpoint):
                shutil.copy2(checkpoint, os.path.join(target_dir, f"{name}.ckpt"))
                line += ", checkpoint installed"
            else:
                line += ", checkpoint NOT FOUND (training may still be running)"

        print(line)

    print(f"\nInstalled under {METABOLISM_DIR}")


if __name__ == "__main__":
    main()
