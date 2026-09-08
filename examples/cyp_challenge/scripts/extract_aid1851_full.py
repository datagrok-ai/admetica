"""Re-extract PubChem AID 1851 with the columns the original export dropped.

`data/raw/veith.csv` holds fitted potencies for the four challenge isoforms, taken from the
Active rows only. The assay carries more than that:

  - a fifth panel, CYP2C19, which no challenge endpoint scores but which trains the encoder;
  - Inconclusive rows that nonetheless carry a fitted potency - weak or partial curves, which
    are information rather than noise once they are weighted;
  - a curve class per measurement, so a clean 15-point fit and a single point of activity stop
    counting the same.

Input: the full AID 1851 data table (~23 MB)
    curl -o aid1851_full.csv "https://pubchem.ncbi.nlm.nih.gov/assay/pcget.cgi?query=download\
&record_type=datatable&actvty=all&response_type=save&aid=1851"

Usage:
    python examples/cyp_challenge/scripts/extract_aid1851_full.py --table aid1851_full.csv
"""

import argparse
import os

import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(BASE, "data", "raw", "aid1851_extended.csv")

SENTINEL = 1e5          # Potency values at or above this mark an unfittable row
PANELS = {
    "p450-cyp1a2": "cyp1a2",
    "p450-cyp2c9": "cyp2c9",
    "p450-cyp2d6": "cyp2d6",
    "p450-cyp3a4": "cyp3a4",
    "p450-cyp2c19": "cyp2c19",   # not scored; an auxiliary head only
}

# NCGC curve classes. Negative classes are signal loss, i.e. inhibition; positive classes are
# activation and must not enter an inhibition model.
CURVE_WEIGHTS = {
    -1.1: 1.00,   # complete curve, high efficacy
    -1.2: 1.00,   # complete curve, partial efficacy
    -2.1: 0.70,   # partial curve, high efficacy
    -2.2: 0.70,   # partial curve, partial efficacy
    -1.3: 0.40,
    -1.4: 0.40,   # complete curve, poor fit
    -2.3: 0.40,
    -2.4: 0.40,   # partial curve, poor fit
    -3.0: 0.15,   # single point of activity: fitted, but not trustworthy
}


def canonical(smiles):
    mol = Chem.MolFromSmiles(smiles) if isinstance(smiles, str) else None
    return Chem.MolToSmiles(mol) if mol is not None else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", required=True, help="full AID 1851 data table CSV")
    parser.add_argument("--out", default=OUT_PATH)
    args = parser.parse_args()

    table = pd.read_csv(args.table, low_memory=False)
    table = table[table["Panel ID"].astype(str).str.isdigit()]
    table["Potency"] = pd.to_numeric(table.Potency, errors="coerce")
    table["Fit_CurveClass"] = pd.to_numeric(table.Fit_CurveClass, errors="coerce")

    usable = table.Potency.notna() & table.Potency.lt(SENTINEL)
    inhibition = table.Fit_CurveClass.isin(CURVE_WEIGHTS)
    table = table[usable & inhibition].copy()

    # Potency is in micromolar; pAC50 = 6 - log10(uM)
    table["pac50"] = 6 - np.log10(table.Potency)
    table["weight"] = table.Fit_CurveClass.map(CURVE_WEIGHTS)
    table["endpoint"] = table["Panel Name"].map(PANELS)
    table["SMILES"] = [canonical(s) for s in table.PUBCHEM_EXT_DATASOURCE_SMILES]
    table = table.dropna(subset=["SMILES", "endpoint"])

    # weighted mean per compound and isoform, so replicate rows collapse by curve quality
    grouped = table.groupby(["SMILES", "endpoint"]).apply(
        lambda g: pd.Series({
            "pac50": np.average(g.pac50, weights=g.weight),
            "weight": g.weight.max(),
        }), include_groups=False).reset_index()

    wide = grouped.pivot(index="SMILES", columns="endpoint", values=["pac50", "weight"])
    wide.columns = [f"{'pac50' if a == 'pac50' else 'weight'}_{b}" for a, b in wide.columns]
    wide = wide.reset_index()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    wide.to_csv(args.out, index=False)

    print(f"{len(wide)} compounds\n")
    print(f"  {'column':18} {'n':>7} {'mean':>8} {'sd':>8} {'mean weight':>12}")
    for endpoint in PANELS.values():
        column = f"pac50_{endpoint}"
        if column not in wide:
            continue
        values = wide[column].dropna()
        weights = wide[f"weight_{endpoint}"].dropna()
        marker = "" if endpoint != "cyp2c19" else "  <- auxiliary only"
        print(f"  {column:18} {len(values):7d} {values.mean():8.3f} {values.std():8.3f}"
              f" {weights.mean():12.2f}{marker}")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
