# Admetica

It is an open-source global effort with collaborators from academia, biotech startups and big pharma.

Our goal is to improve ADMET (Absorption, Distribution, Metabolism, and Excretion) prediction tools.

We welcome everyone with the expertise in the field. If you're interested in collaboration, contact us via [email](mailto:oserhiienko@datagrok.ai) or [LinkedIn](https://www.linkedin.com/in/oleksandra-serhiienko-674ab6239).

## Table of Contents

- [Goals](#goals)
- [Integration with Datagrok](#integration-with-datagrok)
- [Available predictive models](#available-predictive-models)
  - [Absorption](#absorption)
  - [Distribution](#distribution)
  - [Metabolism](#metabolism)
  - [Excretion](#excretion)
- [Comparison of Admetica and Novartis models](#comparison-of-admetica-and-novartis-models)
- [Usage](#usage)
  - [Installation](#installation)
  - [Data](#data)
  - [Training](#training)
  - [Predicting](#predicting)
- [References](#references)

Our goal is to provide a tool that is:

- **Accurate**: It has higher characteristics compared to other open-source tools such as ADMETLab, Chemprop, QikProp etc.
- **Open-source**: The source code is freely available for anyone to view, use, modify and distribute.
- **With simple API**: It has an easy-to-use interface and can be integrated into various applications and platforms.
- **Reproducible**: You can access data sources, modeling workflow notebooks and models to easily reproduce and verify the entire modeling process.
- **Easily deployable**: It is easy to set up and use.
- **Performant**: It offers a reliable and high-performance solution for datasets of all sizes.

## Integration with Datagrok

Our tool easily works with many platforms and applications. With the [Admetica package](https://github.com/datagrok-ai/public/tree/master/packages/Admetica) developed at Datagrok, you can:

- **Mix your data:** Combine your data with Datagrok's collected experimental data for customized predictive models.

- **Visualize results:** Use Datagrok tools for better predictions, data analysis and data visualization.

## Available predictive models

Currently, we have a total of 32 predictive models developed for [Absorption](#absorption), [Distribution](#distribution), [Metabolism](#metabolism), [Excretion](#excretion) and Toxicity.

### Absorption

#### Classification models

Name | Model | Size | Specificity | Sensitivity | Accuracy | Balanced Accuracy | ROC AUC |
|-|-|-|-|-|-|-|-|
| [Pgp-Inhibitor](./absorption/absorption.md#pgp-inhibitor) | Chemprop | 1,275 | 0.877 | 0.923 |  0.904 | 0.902 | ![pgp_inhibitor_roc](./images/Pgp-Inhibitor.PNG) |
| [Pgp-Substrate](./absorption/absorption.md#pgp-substrate) | Chemprop | 332 | 0.786 | 0.820 |  0.807 | 0.803 | ![pgp_substrate_roc](./images/Pgp-Substrate.PNG) |

#### Regression models

Name | Model | Size | MAE | RMSE | R2 | Spearman | Observed vs. Predicted |
|-|-|-|-|-|-|-|-|
| [Caco2](./absorption/absorption.md#caco-2) | Chemprop | 910 | 0.417 | 0.528 | 0.408 | 0.816 | ![Caco2 Observed vs. Predicted plot](./images/caco2_wang_observed_vs_pred.png) |
| [Lipophilicity](./absorption/absorption.md#lipophilicity) | Chemprop | 4200 | 0.456 | 0.612 | 0.734 | 0.842 | ![Lipophilicity Observed vs. Predicted plot](./images/lipophilicity_astrazeneca_observed_vs_pred.png) |
| [Solubility](./absorption/absorption.md#solubility) | Chemprop | 9982 | 0.825 | 1.118 | 0.762 | 0.852 | ![Solubility Observed vs. Predicted plot](./images/solubility_aqsoldb_observed_vs_pred.png) |

### Distribution

#### Regression models

Name | Model | Size | MAE | RMSE | R2 | Spearman | Observed vs. Predicted |
|-|-|-|-|-|-|-|-|
| [PPBR](./distribution/distribution.md#ppbr) | Chemprop | 2790 | 7.945 | 11.642 | 0.410 | 0.650 | ![PPBR Observed vs. Predicted plot](./images/ppbr_az_observed_vs_pred.png) |
| [VDss](./distribution/distribution.md#vdss) | Chemprop | 1130 | 3.100 | 5.232 | 0.069 | 0.500 | ![VDss Observed vs. Predicted plot](./images/vdss_lombardo_observed_vs_pred.png) |

### Metabolism

#### Classification models

Name | Model | Size | Specificity | Sensitivity | Accuracy | Balanced Accuracy | ROC AUC
|-|-|-|-|-|-|-|-|
| [CYP1A2-Inhibitor](./absorption/absorption.md#cyp1a2-inhibitor) | Chemprop | 13,239 | 0.899 | 0.956 |  0.925 | 0.928 | ![cyp1a2_inhibitor_roc](./images/CYP1A2-Inhibitor.PNG) |
| [CYP3A4-Inhibitor](./absorption/absorption.md#cyp3a4-inhibitor) | Chemprop | 12,997 | 0.861 | 0.949 |  0.896 | 0.905 | ![cyp3a4_inhibitor_roc](./images/CYP3A4-Inhibitor.PNG) |
| [CYP3A4-Substrate](./absorption/absorption.md#cyp3a4-substrate) | Chemprop | 1,149 | 0.562 | 0.857 |  0.776 | 0.709 | ![cyp3a4_substrate_roc](./images/CYP3A4-Substrate.PNG) |
| [CYP2C19-Inhibitor](./absorption/absorption.md#cyp2c19-inhibitor) | Chemprop | 13,427 | 0.887 | 0.890 |  0.888 | 0.889 | ![cyp2c19_inhibitor_roc](./images/CYP2C19-Inhibitor.PNG) |
| [CYP2C9-Inhibitor](./absorption/absorption.md#cyp2c9-inhibitor) | Chemprop | 12,881 | 0.899 | 0.880 |  0.893 | 0.890 | ![cyp2c9_inhibitor_roc](./images/CYP2C9-Inhibitor.PNG) |
| [CYP2C9-Substrate](./absorption/absorption.md#cyp2c9-substrate) | Chemprop | 899 | 0.831 | 0.730 |  0.790 | 0.781 | ![cyp2c9_substrate_roc](./images/CYP2C9-Substrate.PNG) |
| [CYP2D6-Inhibitor](./absorption/absorption.md#cyp2d6-inhibitor) | Chemprop | 11,127 | 0.723 | 0.926 |  0.763 | 0.824 | ![cyp2d6_inhibitor_roc](./images/CYP2D6-Inhibitor.PNG) |
| [CYP2D6-Substrate](./absorption/absorption.md#cyp2d6-substrate) | Chemprop | 941 | 0.853 | 0.783 |  0.819 | 0.818 | ![cyp2d6_substrate_roc](./images/CYP2D6-Substrate.PNG) |

Here is a line chart illustrating various metrics for each of the corresponding models.

![comparison_metabolism](./images/metabolism_linechart.png)

### Excretion

#### Regression models

Name | Model | Size | MAE | RMSE | R2 | Spearman | Observed vs. Predicted |
|-|-|-|-|-|-|-|-|
| [Half Life](./excretion/excretion.md#half-life) | Chemprop | 667 | 9.947 | 21.780 | -0.007 | 0.208 | ![Half Life Observed vs. Predicted plot](./images/half_life_obach_observed_vs_pred.png) |
| [Clearance Hepatocyte](./excretion/excretion.md#hepatocyte) | Chemprop | 1213 | 35.930 | 45.848 | 0.088 | 0.379 | ![Clearance Hepatocyte Observed vs. Predicted plot](./images/clearance_hepatocyte_az_observed_vs_pred.png) |
| [Clearance Microsome](./excretion/excretion.md#microsome) | Chemprop | 1102 | 21.797 | 35.914 | 0.305 | 0.573 | ![Clearance Microsome True vs. Predicted plot](./images/clearance_microsome_az_observed_vs_pred.png) |

## Comparison of Admetica and Novartis models

For the comparison, we utilized the surrogate dataset provided in the paper [Application of machine learning models for property prediction to targeted protein degraders](https://www.nature.com/articles/s41467-024-49979-3). This dataset includes publicly available structures and their predicted properties generated by the Novartis machine learning model.

### Cytochrome P450

### Pipeline

We generated test datasets using data from the ChEMBL database. To ensure the test set was representative and produced accurate results, the data was preprocessed using the following steps:

* **Extracting common structures**:  
  
  We compared the Novartis and ChEMBL datasets to identify shared molecular structures. Additionally, we filtered out values that overlapped with the Admetica training set to prevent redundancy.

* **Filtering the ChEMBL dataset**:  
  We removed duplicate entries, prioritizing those labeled as IC50. We also excluded rows with undesired types such as Drug metabolism, FC, Retention_time, T1/2, mechanism based inhibition, Stability etc.

* **Processing values**:  
  We standardized key values for consistency.

  | **Type**                | **Action**                                      |
  |-------------------------|-------------------------------------------------|
  | IC50, AC50, KI, Potency  | Converted to µM by dividing the values by 1000 |
  | Inhibition   | Classified as binary: |
  | | Greater than 50%: `1` |
  | | Less than 50%: `0`    |
  | Other values | Left unchanged (already in µM) |

Both the original ChEMBL dataset and the processed data are available in the [comparison](./comparison/novartis/chembl/) folder. Additionally, the folder contains a Jupyter notebook, [preprocessing_pipeline.ipynb](./comparison/preprocessing_pipeline.ipynb), which fully reproduces the preprocessing steps and obtained datasets.

### 3A4

After performing the pipeline for ChEMBL 3A4, we obtained a dataset structured as follows:

| **Class** | **Number of Entries** |
|-----------|-----------------------|
| Inhibitor   | 549                   |
| Non-Inhibitor   | 239                   |

We conducted comprehensive calculations of ADMET properties and assessed the performance metrics for both the Admetica and Novartis models, resulting in the following outcomes:

| **Metric**                | **Admetica**   | **Novartis**   |
|---------------------------|-----------------------|-----------------------|
| True Positives (TP)      | 134.0                 | 159.0                 |
| True Negatives (TN)      | 368.0                 | 352.0                 |
| False Positives (FP)     | 181.0                 | 197.0                 |
| False Negatives (FN)     | 105.0                 | 80.0                  |
| Sensitivity (Recall)     | 0.5607                | 0.6653                |
| Specificity              | 0.6703                | 0.6412                |
| Balanced Accuracy         | 0.6155                | 0.6532                |
| AUC                       | 0.6155                | 0.6532                |

![3A4 Admetica vs. Novartis](./images/3a4_nx_admetica.png)

These results indicate that the Novartis model performed better overall, leading us to decide to further train our model using their dataset to enhance its predictive capabilities.

### 2C9

After performing the pipeline for ChEMBL 2C9, we obtained a dataset structured as follows:

| **Class** | **Number of Entries** |
|-----------|-----------------------|
| Inhibitor   | 329                   |
| Non-Inhibitor   | 135                   |

We conducted comprehensive calculations of ADMET properties and assessed the performance metrics for both the Admetica and Novartis models, resulting in the following outcomes:

| **Metric**                | **Admetica**    | **Novartis**   |
|---------------------------|-----------------------|-----------------------|
| True Positives (TP)      | 102.0                 | 69.0                  |
| True Negatives (TN)      | 137.0                 | 236.0                 |
| False Positives (FP)     | 192.0                 | 93.0                  |
| False Negatives (FN)     | 33.0                  | 66.0                  |
| Sensitivity (Recall)     | 0.7556                | 0.5111                |
| Specificity              | 0.4164                | 0.7173                |
| Balanced Accuracy         | 0.5860                | 0.6142                |
| AUC                       | 0.5860                | 0.6142                |

![2C9 Admetica vs. Novartis](./images/2c9_nx_admetica.png)

These results indicate that the Novartis model performed better overall, leading us to decide to further train our model using their dataset to enhance its predictive capabilities.

### 2D6

After performing the pipeline for ChEMBL 2D6, we obtained a dataset structured as follows:

| **Class** | **Number of Entries** |
|-----------|-----------------------|
| Inhibitor   | 444                   |
| Non-Inhibitor   | 195                   |

We conducted comprehensive calculations of ADMET properties and assessed the performance metrics for both the Admetica and Novartis models, resulting in the following outcomes:

| **Metric**                | **Admetica**   | **Novartis**   |
|---------------------------|-----------------------|-----------------------|
| True Positives (TP)      | 88.0                  | 55.0                  |
| True Negatives (TN)      | 329.0                 | 403.0                 |
| False Positives (FP)     | 115.0                 | 41.0                  |
| False Negatives (FN)     | 107.0                 | 140.0                 |
| Sensitivity (Recall)     | 0.4513                | 0.2821                |
| Specificity              | 0.7410                | 0.9077                |
| Balanced Accuracy         | 0.5961                | 0.5949                |
| AUC                       | 0.5961                | 0.5949                |

![2D6 Admetica vs. Novartis](./images/2d6_nx_admetica.png)

Given these results, we decided to continue with the Admetica model in its current form, as it demonstrated better performance overall.

The comparison is fully reproducible, and you can find the Jupyter notebook, [comparison_cyp.ipynb](./comparison/comparison_cyp.ipynb), in the folder.

## Usage

### Installation

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chemprop)](https://badge.fury.io/py/chemprop)
[![Chemprop PyPI version](https://badge.fury.io/py/chemprop.svg)](https://badge.fury.io/py/chemprop)

Admetica is a powerful tool for making ADMET predictions and can be easily installed on any operating system. You can install it using pip, and optionally, you can set up a conda environment for better package management.

#### Creating a Conda Environment (Optional)

To create a new conda environment and install Admetica, use the following commands:

```bash
conda create --name admetica-env python=3.11
conda activate admetica-env
```

#### Installing Admetica

To install Admetica, run:

```bash
pip install admetica==1.3
```

By default, the pip installation will include all necessary dependencies for making ADMET predictions.

### Making Predictions

Admetica provides a command-line interface to make predictions. To use it, run:

```bash
admetica_predict \
    --dataset-path data.csv \
    --smiles-column smiles \
    --properties Caco2,PPBR \
    --save-path predictions.csv
```

This command assumes the presence of a file named `data.csv` with SMILES strings in the column `smiles`. In addition, you should specify the properties to be calculated (e.g. `Caco2`). The predictions will be saved to `predictions.csv`.

All models available in the repository are included and can be used.

### Data

In order to train a model or obtain predictions, you must provide data containing molecules (as SMILES strings) and known target values.

The data used in this research and [its overview](./docs/datasets.md) can be found in the `Datasets` folder.

### Training

You can create a model on your own using [chemprop](https://github.com/chemprop/chemprop/blob/master/README.md#training) module or use publicly available models that are licalted in the `Models` folder.

### Predicting

To load a trained model and make predictions, run all the commands specified in the `Chemical Property Prediction and Evaluation.ipynb` file.

## References

Our project is about improving and combining existing solutions, not reinventing the wheel. Here is the list of resources we've investigated:

1. ADMETlab: a platform for systematic ADMET evaluation based on a comprehensively collected ADMET database / Jie Dong, Ning-Ning Wang, Zhi-Jiang Yao та ін. // J Cheminform. – 2018. – <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6020094/>.
2. Evaluation of Free Online ADMET Tools for Academic or Small Biotech Environments / Júlia Dulsat, Blanca López-Nieto, Roger Estrada-Tejedor, José I. Borrell // Molecules. – 2023. – <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9864198/>.
3. Vishwesh Venkatraman. FP-ADMET: a compendium of fingerprint-based ADMET prediction models / Vishwesh Venkatraman // J Cheminform. – 2021. – <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8479898/>.
4. Front Pharmacol. vNN Web Server for ADMET Predictions / Front Pharmacol // Front Pharmacol. – 2017. – <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5722789/>.
5. ADMETlab 2.0: an integrated online platform for accurate and comprehensive predictions of ADMET properties / Guoli Xiong, Zhenxing Wu, Jiacai Yi та ін. // Nucleic Acids Res. – 2021. – <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8262709/>.
6. In silico Prediction of Chemical Ames Mutagenicity / Congying Xu, Feixiong Cheng, Lei Chen та ін. // J Cheminform. – 2012. – <https://pubs.acs.org/doi/abs/10.1021/ci300400a>.
7. Computational Models for Human and Animal Hepatotoxicity with a Global Application Scope / Denis Mulliner, Friedemann Schmidt, Manuela Stolte та ін. // Chem. Res. Toxicol.. – 2016. – <https://pubs.acs.org/doi/10.1021/acs.chemrestox.5b00465>.
8. ADMET Evaluation in Drug Discovery. 16. Predicting hERG Blockers by Combining Multiple Pharmacophores and Machine Learning Approaches / Shuangquan Wang, Huiyong Sun, Hui Liu та ін. // Mol. Pharmaceutics. – 2016. – <https://pubs.acs.org/doi/10.1021/acs.molpharmaceut.6b00471>.
