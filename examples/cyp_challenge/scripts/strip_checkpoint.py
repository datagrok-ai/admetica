"""Drop optimizer state from a trained checkpoint.

Lightning stores the optimizer and scheduler state alongside the weights, which roughly triples
the file. Nothing outside training reads them, so a checkpoint that only has to make predictions
can lose them: the weights, hyper-parameters and target scaler are untouched and predictions stay
bit-identical.

Usage:
    python examples/cyp_challenge/scripts/strip_checkpoint.py results/*/models/*.ckpt
"""

import argparse
import os

import torch

DROP = ["optimizer_states", "lr_schedulers", "callbacks", "loops"]


def strip(path, suffix):
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    kept = {k: v for k, v in checkpoint.items() if k not in DROP}

    out = path if suffix is None else path.replace(".ckpt", f"{suffix}.ckpt")
    before = os.path.getsize(path) / 1e6
    torch.save(kept, out)
    after = os.path.getsize(out) / 1e6
    dropped = [k for k in DROP if k in checkpoint]
    print(f"{out}: {before:.0f} MB -> {after:.0f} MB (dropped {', '.join(dropped) or 'nothing'})")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoints", nargs="+")
    parser.add_argument("--suffix", default=None,
                        help="write alongside the original instead of replacing it")
    args = parser.parse_args()

    for path in args.checkpoints:
        strip(path, args.suffix)


if __name__ == "__main__":
    main()
