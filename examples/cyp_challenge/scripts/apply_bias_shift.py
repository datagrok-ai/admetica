"""Apply the per-isoform bias correction to a submission file.

Shifts are the soft-RAE-optimal constants on the champion's out-of-fold predictions, stable
across all five CV folds (see results/bias_shift/check.txt); they correct the systematic
under-prediction the pooled qHTS training data introduces.

Usage:
    python examples/cyp_challenge/scripts/apply_bias_shift.py
"""

import os

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_PATH = os.path.join(BASE, "cyp_challenge_submission_final.csv")
OUT_PATH = os.path.join(BASE, "results", "bias_shift", "cyp_challenge_submission_bias_shifted.csv")

SHIFTS = {"CYP1A2": 0.24, "CYP2C9": 0.16, "CYP2D6": 0.04, "CYP3A4": 0.16}


def main():
    sub = pd.read_csv(IN_PATH)
    for cyp, shift in SHIFTS.items():
        sub[f"{cyp}_pIC50_direct_inhibition"] += shift

    values = sub[[f"{c}_pIC50_direct_inhibition" for c in SHIFTS]].to_numpy()
    assert len(sub) == 750 and np.isfinite(values).all()
    assert not sub.Molecule_Name.duplicated().any()

    sub.to_csv(OUT_PATH, index=False)
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
