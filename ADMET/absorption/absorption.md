# Absorption

Absorption is the process by which drugs enter the bloodstream after administration. It is pivotal in pharmaceutical research, enabling enhanced bioavailability, precise dosing, formulation optimization, reduced variability among patient populations, and minimized side effects. In this part, we studied 3 absorption-related endpoints.

## Table of Contents

- [Pgp-Inhibitor](#pgp-inhibitor)
- [Pgp-Substrate](#pgp-substrate)
- [Bioavailability](#bioavailability)
- [Caco-2](#caco-2)
- [Lipophilicity](#lipophilicity)
- [Solubility](#solubility)
- [Data comparison](#data-comparison)

## Pgp-Inhibitor

It is a probability of being an inhibitor of P-glycoprotein which is responsible for cell membrane transport. Inhibiting Pgp leads to low cell permeability of substance.

The Pgp-Inhibitor dataset combines data from two sources, comprising 1,275 compounds, with 666 classified as inhibitors and 609 as non-inhibitors.

Results on dataset (higher is better).

| Dataset | Size | Specificity | Sensitivity | Accuracy | Balanced Accuracy |
|-|-|-|-|-|-|
| Pgp-Inhibitor | 1,275 | 0.877 | 0.927 |  0.904 | 0.902 |

![Pgp-Inhibitor](../../images/Pgp-Inhibitor.PNG)

## Pgp-Substrate

It is a probability of being a substrate of P-glycoprotein which is responsible for cell membrane permeability. Compounds with high molecular mass and a large number of polar atoms are the most probable substrates. Binding the substrate leads to low cell permeability of substance.

The Pgp-Substrate dataset is derived from a single source, encompassing 332 compounds, of which 126 are substrates, and 206 are non-substrates.

Results on dataset (higher is better).

| Dataset | Size | Specificity | Sensitivity | Accuracy | Balanced Accuracy |
|-|-|-|-|-|-|
| Pgp-Substrate | 332 | 0.786 | 0.820 |  0.807 | 0.803 |

![Pgp-Substrate](../../images/Pgp-Substrate.PNG)

## Bioavailability

The range of bioavailability value is 0-100. One threshold (30%) was applied in order to split compounds into posititve and negative. A probability that less than 30% of substance reaches systemic circulation.

Overall, the dataset contains 986 compounds, where positive category contains 660 compounds and negative 326.

## Caco-2

The human colon epithelial cancer cell line, Caco-2, is used as an in vitro model to simulate the human intestinal tissue. The experimental result on the rate of drug passing through the Caco-2 cells can approximate the rate at which the drug permeates through the human intestinal tissue.

Dataset | Size | MAE | RMSE | R2 | Spearman |
|-|-|-|-|-|-|
| Caco2 | 910 | 0.417 | 0.528 | 0.408 | 0.816 |

### Observed vs. Predicted plot

![Caco2 Observed vs. Predicted plot](../../images/caco2_wang_observed_vs_pred.png)

## Lipophilicity

Lipophilicity measures the ability of a drug to dissolve in a lipid (e.g. fats, oils) environment. High lipophilicity often leads to high rate of metabolism, poor solubility, high turn-over, and low absorption. From MoleculeNet.

Dataset | Size | MAE | RMSE | R2 | Spearman |
|-|-|-|-|-|-|
| Lipophilicity | Chemprop | 4200 | 0.456 | 0.612 | 0.734 | 0.842 |

### Observed vs. Predicted plot

![Lipophilicity Observed vs. Predicted plot](../../images/lipophilicity_astrazeneca_observed_vs_pred.png)

## Solubility

Aqeuous solubility measures a drug's ability to dissolve in water. Poor water solubility could lead to slow drug absorptions, inadequate bioavailablity and even induce toxicity. More than 40% of new chemical entities are not soluble.

Dataset | Size | MAE | RMSE | R2 | Spearman |
|-|-|-|-|-|-|
| Solubility | Chemprop | 9982 | 0.825 | 1.118 | 0.762 | 0.852 |

### Observed vs. Predicted plot

![Solubility True vs. Predicted plot](../../images/solubility_aqsoldb_observed_vs_pred.png)

## Data comparison

Name | Size | Processed size | TDC size | TDC processed size | Common | Resulting |
|-|-|-|-|-|-|-|
| Pgp-Inhibitor | 1275 | 1227 | 1218 | 1218 | 1218 | 1227 |
| Pgp-Substrate | 332 | 332 | - | - | - | 332 |
| Bioavailability | 986 | 985 | 640 | 640 | 296 |  |
| Caco-2 | 910 | 910 | 910 | 910 | 910 | 910 |
| HIA | 769 | 769 | 578 | 578 | 578 | 769 |
| Lipophilicity | 4200 | 4192 | 4200 | 4192 | 4192 | 4192 |
