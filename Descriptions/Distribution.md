# Distribution

Distribution refers to the process of transporting a drug from its point of entry into the bloodstream to its target organs, tissues, or specific sites where it exerts its therapeutic effects, with factors such as drug properties and physiological characteristics influencing this process.

## Table of Contents

- [BBB](#bbb)
- [PPBR](#ppbr)
- [VDss](#vdss)
- [Data comparison](#data-comparison)

## BBB

It is a probability of expected blood to brain ratio of compound to be less than 0.1. The low ratio represents not efficient distribution which is frequently happens to massive structures.

The BBB dataset combines data from three sources, totaling 27,796 compounds, with 8,508 classified as BBB+ and 19,288 as BBB-. This dataset provides valuable insights into blood-brain barrier penetration.

## PPBR

The human plasma protein binding rate (PPBR) is expressed as the percentage of a drug bound to plasma proteins in the blood. This rate strongly affect a drug's efficiency of delivery. The less bound a drug is, the more efficiently it can traverse and diffuse to the site of actions.

| Name | Size | MAE | RMSE | R2 | Spearman |
|-|-|-|-|-|-|
| PPBR | 2790 | 7.945 | 11.642 | 0.410 | 0.650 |

### Observed vs. Predicted plot

![PPBR True vs. Predicted plot](../images/ppbr_az_observed_vs_pred.png)

## VDss

The volume of distribution at steady state (VDss) measures the degree of a drug's concentration in body tissue compared to concentration in blood. Higher VD indicates a higher distribution in the tissue and usually indicates the drug with high lipid solubility, low plasma protein binidng rate.

| Name | Size | MAE | RMSE | R2 | Spearman |
|-|-|-|-|-|-|
| VDss | 1130 | 3.100 | 5.232 | 0.069 | 0.500 |

### True vs. Predicted plot

![VDss Observed vs. Predicted plot](../images/vdss_lombardo_observed_vs_pred.png)

## Data comparison

Name | Size | Processed size | TDC size | TDC processed size | Common | Resulting |
|-|-|-|-|-|-|-|
| PPBR | 2790 | 2782 | 1614 | 1607 | 1607 | 2782 |
| VDss | 1130 | 1125 | 1130 | 1125 | 1125 | 1125 |
| BBB | 27791 | 27716 | 2030 | 2029 | 2029 | 27716 |
