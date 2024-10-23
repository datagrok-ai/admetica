# Toxicity

Toxicity measures how much damage a drug could cause to organisms.

## Table of Contents

- [LD50](#ld50)
- [Data comparison](#data-comparison)

## LD50

Acute toxicity LD50 measures the most conservative dose that can lead to lethal adverse effects. The higher the dose, the more lethal of a drug.

| Name | Size | MAE | RMSE | R2 | Spearman |
|-|-|-|-|-|-|
| LD50 | 7282 | 0.437 | 0.609 | 0.596 | 0.745 |

### Observed vs. Predicted plot

![LD50 Observed vs. Predicted plot](../../images/ld50_observed_vs_pred.png)

## hERG

Inhibition of the hERG (human Ether-à-go-go-Related Gene) current causes QT interval prolongation and lead to life threatening arrhythmia. Inhibition of hERG is considered as precaution.

| Name | Size | Specificity | Sensitivity | Accuracy | Balanced Accuracy |
|-|-|-|-|-|-|
| hERG | 22,249 | 0.811 | 0.897 | 0.885 |  0.854  |

![hERG](../../images/herg_roc.png)

## Data comparison

| Name | Size | Processed size | TDC size | TDC processed size | Common | Resulting |
|-|-|-|-|-|-|-|
| hERG | 22263 | 22248 | - | - | - | 22248 |
| H-HT | 2171 | 2170 | - | - | - | 2170 |
| Ames | 8085 | 7742 | - | - | - | 7742 |
| SkinSen | 739 | 549 | - | - | - | 549 |
| LD50 | 7385 | 7282 | - | - | - | 7282 |
