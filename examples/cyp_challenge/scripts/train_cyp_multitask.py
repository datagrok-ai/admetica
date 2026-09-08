"""Multi-task CYP training: one model with four outputs instead of four separate models.

Chemprop masks missing targets, so a compound measured for one isoform still trains the shared
encoder. `--pretrained` warm-starts that encoder from CheMeleon weights, which is what made task
sharing help rather than hurt. One fold per invocation, so folds can run in parallel.

Usage:
    python examples/cyp_challenge/scripts/train_cyp_multitask.py --fold 1
    python examples/cyp_challenge/scripts/train_cyp_multitask.py --production
    python examples/cyp_challenge/scripts/train_cyp_multitask.py --fold 1 --pretrained chemeleon_mp.pt
"""

import argparse
import hashlib
import os
import time

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import spearmanr
from lightning import pytorch as pl
from lightning.pytorch.callbacks import Callback, EarlyStopping, ModelCheckpoint
from chemprop import data, featurizers, models, nn
from rdkit import RDLogger

RDLogger.DisableLog("rdApp.*")

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(os.path.dirname(CHALLENGE_DIR))
DATA_DIR = os.path.join(CHALLENGE_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "processed", "multisource_pac50.csv")
DEFAULT_WORK_DIR = os.path.join(CHALLENGE_DIR, "results", "chemeleon_multitask")

ENDPOINTS = ["cyp1a2", "cyp2c9", "cyp2d6", "cyp3a4"]
# Auxiliary columns train the shared encoder but never reach the scored output.
SCORED = [f"challenge_{e}" for e in ENDPOINTS]

# Matched to the single-task runs so the comparison is like for like
NUM_FOLDS = 5
MAX_EPOCHS = 60
PATIENCE = 10
VAL_FRACTION = 0.1
RANDOM_STATE = 42

featurizer = featurizers.SimpleMoleculeMolGraphFeaturizer()


def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


class EpochLogger(Callback):
    """One line per epoch, so long runs report progress in their log file."""

    def on_validation_epoch_end(self, trainer, module):
        val = trainer.callback_metrics.get("val_loss")
        log(f"epoch {trainer.current_epoch + 1}/{trainer.max_epochs}"
            + (f" val_loss={float(val):.4f}" if val is not None else ""))


def build_loader(datapoints, scaler=None, shuffle=True):
    dset = data.MoleculeDataset(datapoints, featurizer)
    fitted = dset.normalize_targets() if scaler is None else dset.normalize_targets(scaler)
    return data.build_dataloader(dset, num_workers=0, shuffle=shuffle), fitted


def build_model(scaler, n_tasks, pretrained=None):
    """One output per source and isoform; encoder optionally warm-started from pretrained weights."""
    if pretrained:
        checkpoint = torch.load(pretrained, weights_only=True)
        message_passing = nn.BondMessagePassing(**checkpoint["hyper_parameters"])
        message_passing.load_state_dict(checkpoint["state_dict"])
    else:
        message_passing = nn.BondMessagePassing()

    predictor = nn.RegressionFFN(
        n_tasks=n_tasks,
        output_transform=nn.UnscaleTransform.from_standard_scaler(scaler),
        input_dim=message_passing.output_dim,
        criterion=nn.BoundedMSELoss(),
    )
    return models.MPNN(message_passing, nn.MeanAggregation(), predictor, batch_norm=True,
                       metrics=[nn.metrics.RMSEMetric(), nn.metrics.MAEMetric()])


def make_trainer(max_epochs=MAX_EPOCHS, callbacks=None, accelerator="cpu", checkpointing=False):
    return pl.Trainer(logger=False, enable_checkpointing=checkpointing, enable_progress_bar=False,
                      accelerator=accelerator, devices=1, max_epochs=max_epochs,
                      callbacks=callbacks or [])


def datapoints_from(df, targets, lt):
    """lt marks left-censored targets, where the true value is at most y."""
    # BoundedMSELoss dereferences both masks, so gt_mask must be present even though nothing is
    # right-censored
    gt = np.zeros_like(lt)
    return [data.MoleculeDatapoint.from_smi(s, y, lt_mask=m, gt_mask=g)
            for s, y, m, g in zip(df.SMILES.values, targets, lt, gt)]


def score(observed, predicted):
    return {
        "MAE": mean_absolute_error(observed, predicted),
        "RMSE": float(np.sqrt(mean_squared_error(observed, predicted))),
        "R2": r2_score(observed, predicted),
        "Spearman": spearmanr(observed, predicted).statistic,
    }


def assign_folds(smiles):
    """Fold follows the compound, not its row position, so datasets stay comparable as they grow."""
    return np.array([int(hashlib.md5(f"{RANDOM_STATE}:{s}".encode()).hexdigest(), 16) % NUM_FOLDS
                     for s in smiles])


def run_fold(df, targets, columns, lt, fold, work_dir, pretrained, accelerator="cpu",
             monitor_scored=False):
    assignment = assign_folds(df.SMILES.values)
    test_index = np.where(assignment == fold - 1)[0]
    train_index = np.where(assignment != fold - 1)[0]
    fit_index, val_index = train_test_split(train_index, test_size=VAL_FRACTION,
                                            random_state=RANDOM_STATE)

    val_targets = targets[val_index]
    if monitor_scored:
        # Early stopping listens to the scored heads only: the validation split keeps just the
        # rows with a challenge measurement, and their auxiliary targets are blanked, so val_loss
        # cannot be driven by the (much larger) auxiliary sources.
        scored_cols = [columns.index(c) for c in SCORED]
        keep = ~np.isnan(targets[val_index][:, scored_cols]).all(axis=1)
        val_index = val_index[keep]
        val_targets = targets[val_index].copy()
        aux_cols = [i for i in range(len(columns)) if i not in scored_cols]
        val_targets[:, aux_cols] = np.nan

    train_loader, scaler = build_loader(
        datapoints_from(df.iloc[fit_index], targets[fit_index], lt[fit_index]), shuffle=True)
    val_loader, _ = build_loader(
        datapoints_from(df.iloc[val_index], val_targets, lt[val_index]),
        scaler=scaler, shuffle=False)
    test_loader, _ = build_loader(
        datapoints_from(df.iloc[test_index], targets[test_index], lt[test_index]),
        scaler=scaler, shuffle=False)

    model = build_model(scaler, len(columns), pretrained)
    callbacks = [EpochLogger(),
                 EarlyStopping(monitor="val_loss", mode="min", patience=PATIENCE)]
    checkpoint_cb = None
    if monitor_scored:
        # Keep the best-epoch weights rather than the last ones early stopping ran past.
        checkpoint_cb = ModelCheckpoint(dirpath=os.path.join(work_dir, f"ckpt_fold{fold}"),
                                        monitor="val_loss", mode="min", save_top_k=1)
        callbacks.append(checkpoint_cb)
    trainer = make_trainer(callbacks=callbacks, accelerator=accelerator,
                           checkpointing=monitor_scored)
    started = time.time()
    trainer.fit(model, train_loader, val_loader)
    best_path = checkpoint_cb.best_model_path if checkpoint_cb else None
    predicted = np.concatenate(trainer.predict(model, test_loader, ckpt_path=best_path))

    best_epoch = trainer.current_epoch
    if best_path:
        import re
        found = re.search(r"epoch=(\d+)", os.path.basename(best_path))
        if found:
            best_epoch = int(found.group(1)) + 1

    test = df.iloc[test_index]
    rows, oof = [], []
    for scored_column in SCORED:
        column = columns.index(scored_column)
        endpoint = scored_column.replace("challenge_", "")
        observed = targets[test_index][:, column]
        measured = ~np.isnan(observed)
        if measured.sum() < 30:
            continue

        endpoint_pred = predicted[measured, column]
        endpoint_obs = observed[measured]
        in_domain = np.ones(int(measured.sum()), dtype=bool)

        row = score(endpoint_obs, endpoint_pred)
        row.update(endpoint=endpoint, fold=fold, epochs=best_epoch,
                   n_test=int(measured.sum()), n_challenge=int(measured.sum()))
        row.update({f"challenge_{k}": v for k, v in row.items()
                    if k in ("MAE", "RMSE", "R2", "Spearman")})
        rows.append(row)

        oof.append(pd.DataFrame({
            "endpoint": endpoint, "fold": fold, "SMILES": test.SMILES.values[measured],
            "observed": endpoint_obs, "predicted": endpoint_pred, "is_challenge": in_domain,
        }))

    pd.DataFrame(rows).to_csv(os.path.join(work_dir, f"cv_fold_metrics_fold{fold}.csv"), index=False)
    for frame in oof:
        endpoint = frame.endpoint.iloc[0]
        frame.to_csv(os.path.join(work_dir, f"oof_{endpoint}_fold{fold}.csv"), index=False)

    summary = " ".join(
        f"{r['endpoint'][3:]}={r.get('challenge_Spearman', float('nan')):.3f}" for r in rows)
    log(f"fold {fold}: epochs={trainer.current_epoch} best={best_epoch} in-domain rho — {summary} "
        f"({time.time() - started:.0f}s)")


def run_production(df, targets, columns, lt, work_dir, pretrained, accelerator="cpu"):
    metrics = pd.concat(
        [pd.read_csv(p) for p in
         [os.path.join(work_dir, f"cv_fold_metrics_fold{f}.csv") for f in range(1, NUM_FOLDS + 1)]
         if os.path.exists(p)], ignore_index=True)
    epochs = max(int(metrics.epochs.median()), 1)
    log(f"production model on all {len(df)} compounds for {epochs} epochs")

    loader, scaler = build_loader(datapoints_from(df, targets, lt), shuffle=True)
    model = build_model(scaler, len(columns), pretrained)
    trainer = make_trainer(max_epochs=epochs, accelerator=accelerator)
    trainer.fit(model, loader)

    model_dir = os.path.join(work_dir, "models")
    os.makedirs(model_dir, exist_ok=True)
    path = os.path.join(model_dir, "multitask_pac50.ckpt")
    trainer.save_checkpoint(path)
    log(f"saved {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fold", type=int, choices=range(1, NUM_FOLDS + 1))
    parser.add_argument("--production", action="store_true")
    parser.add_argument("--work-dir", default=DEFAULT_WORK_DIR)
    parser.add_argument("--data", default=DATA_PATH)
    parser.add_argument("--pretrained", default=None,
                        help="path to pretrained message-passing weights, e.g. chemeleon_mp.pt")
    parser.add_argument("--accelerator", default="cpu", choices=["cpu", "mps"],
                        help="mps needs PYTORCH_ENABLE_MPS_FALLBACK=1 for the scatter ops")
    parser.add_argument("--monitor-scored", action="store_true",
                        help="early-stop on the challenge heads' validation loss only, "
                             "and predict with the best epoch's weights")
    args = parser.parse_args()

    os.makedirs(args.work_dir, exist_ok=True)
    df = pd.read_csv(args.data)
    columns = [c for c in df.columns if c != "SMILES" and not c.endswith("__lt")]
    missing = [c for c in SCORED if c not in columns]
    if missing:
        raise SystemExit(f"{args.data} is missing scored columns: {missing}")
    targets = df[columns].to_numpy(dtype=float)
    lt = np.column_stack([df[f"{c}__lt"] if f"{c}__lt" in df.columns else np.zeros(len(df), bool)
                          for c in columns]).astype(bool)
    log(f"{len(df)} compounds, {len(columns)} heads ({len(SCORED)} scored), "
        f"label density {np.mean(~np.isnan(targets)):.1%}"
        + f", {int(lt.sum())} censored"
        + (f", pretrained encoder {os.path.basename(args.pretrained)}" if args.pretrained else ""))

    if args.production:
        run_production(df, targets, columns, lt, args.work_dir, args.pretrained,
                       args.accelerator)
    elif args.fold:
        run_fold(df, targets, columns, lt, args.fold, args.work_dir, args.pretrained,
                 args.accelerator, args.monitor_scored)
    else:
        raise SystemExit("pass --fold N or --production")


if __name__ == "__main__":
    main()
