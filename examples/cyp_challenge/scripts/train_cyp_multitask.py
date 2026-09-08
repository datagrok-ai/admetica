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
import os
import time

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import spearmanr
from lightning import pytorch as pl
from lightning.pytorch.callbacks import EarlyStopping
from chemprop import data, featurizers, models, nn
from rdkit import RDLogger

RDLogger.DisableLog("rdApp.*")

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(os.path.dirname(CHALLENGE_DIR))
DATA_DIR = os.path.join(CHALLENGE_DIR, "data")
DEFAULT_WORK_DIR = os.path.join(CHALLENGE_DIR, "results", "chemeleon_multitask")

ENDPOINTS = ["cyp1a2", "cyp2c9", "cyp2d6", "cyp3a4"]

# Matched to the single-task runs so the comparison is like for like
NUM_FOLDS = 5
MAX_EPOCHS = 60
PATIENCE = 10
VAL_FRACTION = 0.1
RANDOM_STATE = 42

featurizer = featurizers.SimpleMoleculeMolGraphFeaturizer()


def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def build_loader(datapoints, scaler=None, shuffle=True):
    dset = data.MoleculeDataset(datapoints, featurizer)
    fitted = dset.normalize_targets() if scaler is None else dset.normalize_targets(scaler)
    return data.build_dataloader(dset, num_workers=0, shuffle=shuffle), fitted


def build_model(scaler, pretrained=None):
    """Four-output regression head; encoder optionally warm-started from pretrained weights."""
    if pretrained:
        checkpoint = torch.load(pretrained, weights_only=True)
        message_passing = nn.BondMessagePassing(**checkpoint["hyper_parameters"])
        message_passing.load_state_dict(checkpoint["state_dict"])
    else:
        message_passing = nn.BondMessagePassing()

    predictor = nn.RegressionFFN(
        n_tasks=len(ENDPOINTS),
        output_transform=nn.UnscaleTransform.from_standard_scaler(scaler),
        input_dim=message_passing.output_dim,
    )
    return models.MPNN(message_passing, nn.MeanAggregation(), predictor, batch_norm=True,
                       metrics=[nn.metrics.RMSEMetric(), nn.metrics.MAEMetric()])


def make_trainer(max_epochs=MAX_EPOCHS, callbacks=None, accelerator="cpu"):
    return pl.Trainer(logger=False, enable_checkpointing=False, enable_progress_bar=False,
                      accelerator=accelerator, devices=1, max_epochs=max_epochs,
                      callbacks=callbacks or [])


def datapoints_from(df, targets):
    return [data.MoleculeDatapoint.from_smi(s, y) for s, y in zip(df.SMILES.values, targets)]


def score(observed, predicted):
    return {
        "MAE": mean_absolute_error(observed, predicted),
        "RMSE": float(np.sqrt(mean_squared_error(observed, predicted))),
        "R2": r2_score(observed, predicted),
        "Spearman": spearmanr(observed, predicted).statistic,
    }


def run_fold(df, targets, fold, work_dir, pretrained):
    kfold = KFold(n_splits=NUM_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    splits = list(kfold.split(np.arange(len(df))))
    train_index, test_index = splits[fold - 1]
    fit_index, val_index = train_test_split(train_index, test_size=VAL_FRACTION,
                                            random_state=RANDOM_STATE)

    train_loader, scaler = build_loader(
        datapoints_from(df.iloc[fit_index], targets[fit_index]), shuffle=True)
    val_loader, _ = build_loader(
        datapoints_from(df.iloc[val_index], targets[val_index]), scaler=scaler, shuffle=False)
    test_loader, _ = build_loader(
        datapoints_from(df.iloc[test_index], targets[test_index]), scaler=scaler, shuffle=False)

    model = build_model(scaler, pretrained)
    trainer = make_trainer(callbacks=[EarlyStopping(monitor="val_loss", mode="min",
                                                    patience=PATIENCE)])
    started = time.time()
    trainer.fit(model, train_loader, val_loader)
    predicted = np.concatenate(trainer.predict(model, test_loader))

    test = df.iloc[test_index]
    rows, oof = [], []
    for column, endpoint in enumerate(ENDPOINTS):
        observed = targets[test_index][:, column]
        measured = ~np.isnan(observed)
        if measured.sum() < 30:
            continue

        endpoint_pred = predicted[measured, column]
        endpoint_obs = observed[measured]
        in_domain = test[f"{endpoint}_challenge"].values[measured].astype(bool)

        row = score(endpoint_obs, endpoint_pred)
        row.update(endpoint=endpoint, fold=fold, epochs=trainer.current_epoch,
                   n_test=int(measured.sum()), n_challenge=int(in_domain.sum()))
        if in_domain.sum() > 30:
            row.update({f"challenge_{k}": v for k, v in
                        score(endpoint_obs[in_domain], endpoint_pred[in_domain]).items()})
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
    log(f"fold {fold}: epochs={trainer.current_epoch} in-domain rho — {summary} "
        f"({time.time() - started:.0f}s)")


def run_production(df, targets, work_dir, pretrained, accelerator="cpu"):
    metrics = pd.concat(
        [pd.read_csv(p) for p in
         [os.path.join(work_dir, f"cv_fold_metrics_fold{f}.csv") for f in range(1, NUM_FOLDS + 1)]
         if os.path.exists(p)], ignore_index=True)
    epochs = max(int(metrics.epochs.median()), 1)
    log(f"production model on all {len(df)} compounds for {epochs} epochs")

    loader, scaler = build_loader(datapoints_from(df, targets), shuffle=True)
    model = build_model(scaler, pretrained)
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
    parser.add_argument("--pretrained", default=None,
                        help="path to pretrained message-passing weights, e.g. chemeleon_mp.pt")
    parser.add_argument("--accelerator", default="cpu", choices=["cpu", "mps"],
                        help="mps needs PYTORCH_ENABLE_MPS_FALLBACK=1 for the scatter ops")
    args = parser.parse_args()

    os.makedirs(args.work_dir, exist_ok=True)
    df = pd.read_csv(os.path.join(DATA_DIR, "multitask_pac50.csv"))
    targets = df[ENDPOINTS].to_numpy(dtype=float)
    log(f"{len(df)} compounds, label density {np.mean(~np.isnan(targets)):.1%}"
        + (f", pretrained encoder {os.path.basename(args.pretrained)}" if args.pretrained else ""))

    if args.production:
        run_production(df, targets, args.work_dir, args.pretrained, args.accelerator)
    elif args.fold:
        run_fold(df, targets, args.fold, args.work_dir, args.pretrained)
    else:
        raise SystemExit("pass --fold N or --production")


if __name__ == "__main__":
    main()
