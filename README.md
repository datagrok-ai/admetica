# Admetica

It is an open-source global effort with collaborators from academia, biotech startups and big pharma.

Our goal is to improve pharmaceutical research using advanced ADMET (Absorption, Distribution, Metabolism, and Excretion) prediction tools.

We welcome everyone with the expertise in the field. If you are interested in collaboration, feel free to reach us:

- **Email**: [oserhiienko@datagrok.ai](mailto:oserhiienko@datagrok.ai)
- **LinkedIn**: [Oleksandra Serhiienko](https://www.linkedin.com/in/oleksandra-serhiienko-674ab6239)

## Table of Contents

- [Goals](#goals)
- [Using at Datagrok](#using-at-datagrok)
- [Available predictive models](#available-predictive-models)
  - [Absorption](#absorption)
  - [Metabolism](#metabolism)
  - [Distribution](#distribution)
- [Personal use](#personal-use)
  - [Requirements](#requirements)
  - [Data](#data)
  - [Training](#training)
  - [Predicting](#predicting)

## Goals

Our goal is to provide a tool that is:

- **Accurate**: It has higher characteristics compared to other open-source tools such as ADMETLab, Chemprop, QikProp etc.
- **Open-source**: The source code is freely available for anyone to view, use, modify and distribute.
- **With simple API**: It has an easy-to-use interface and can be integrated into various applications and platforms.
- **Reproducible**: You can access data sources, modeling workflow notebooks and models to easily reproduce and verify the entire modeling process.
- **Easily deployable**: It is easy to set up and use.
- **Performant**: It offers a reliable and high-performance solution for datasets of all sizes.

## Using at Datagrok

Datagrok provides:

- **Cutting-edge machine learning models:** We provide cutting-edge machine learning models for accurate ADMET property prediction.

- **Unique data integration capability:** Users can integrate their own experimental data. This empowers researchers to customize and refine predictive models to suit their specific research goals

- **Visual results interpretation:** Datagrok provides an expanded range of tools and functionalities for enhancing predictions, data analysis, and results visualization. It is helpful in interpreting the results.

## Available predictive models

### Absorption

Name | Model | Size | Specificity | Sensitivity | Accuracy | ROC AUC |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| [Pgp-Inhibitor](./Descriptions/Absorption.md#pgp-inhibitor) | Chemprop | 1,275 | 0.8771 | 0.9269 |  0.9038 | ![pgp_inhibitor_roc](./Roc_Auc/Pgp-Inhibitor.PNG) |
| [Pgp-Substrate](./Descriptions/Absorption.md#pgp-substrate) | Chemprop | 332 | 0.7857 | 0.8203 |  0.8072 | ![pgp_substrate_roc](./Roc_Auc/Pgp-Substrate.PNG) |

### Metabolism

Name | Model | Size | Specificity | Sensitivity | Accuracy | ROC AUC
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| [CYP1A2-Inhibitor](./Descriptions/Metabolism.md#cyp1a2-inhibitor) | Chemprop | 13,239 | 0.8991 | 0.9563 |  0.925 | ![cyp1a2_inhibitor_roc](./Roc_Auc/CYP1A2-Inhibitor.PNG) |
| [CYP3A4-Inhibitor](./Descriptions/Metabolism.md#cyp3a4-inhibitor) | Chemprop | 12,997 | 0.8607 | 0.9492 |  0.896 | ![cyp3a4_inhibitor_roc](./Roc_Auc/CYP3A4-Inhibitor.PNG) |
| [CYP3A4-Substrate](./Descriptions/Metabolism.md#cyp3a4-substrate) | Chemprop | 1,149 | 0.5619 | 0.8566 |  0.7755 | ![cyp3a4_substrate_roc](./Roc_Auc/CYP3A4-Substrate.PNG) |
| [CYP2C19-Inhibitor](./Descriptions/Metabolism.md#cyp2c19-inhibitor) | Chemprop | 13,427 | 0.8865 | 0.8895 |  0.8879 | ![cyp2c19_inhibitor_roc](./Roc_Auc/CYP2C19-Inhibitor.PNG) |
| [CYP2C9-Inhibitor](./Descriptions/Metabolism.md#cyp2c9-inhibitor) | Chemprop | 12,881 | 0.8991 | 0.8797 |  0.8929 | ![cyp2c9_inhibitor_roc](./Roc_Auc/CYP2C9-Inhibitor.PNG) |
| [CYP2C9-Substrate](./Descriptions/Metabolism.md#cyp2c9-substrate) | Chemprop | 899 | 0.8314 | 0.7302 |  0.7899 | ![cyp2c9_substrate_roc](./Roc_Auc/CYP2C9-Substrate.PNG) |
| [CYP2D6-Inhibitor](./Descriptions/Metabolism.md#cyp2d6-inhibitor) | Chemprop | 11,127 | 0.7226 | 0.9252 |  0.7630 | ![cyp2d6_inhibitor_roc](./Roc_Auc/CYP2D6-Inhibitor.PNG) |
| [CYP2D6-Substrate](./Descriptions/Metabolism.md#cyp2d6-substrate) | Chemprop | 941 | 0.8529 | 0.783 |  0.8185 | ![cyp2d6_substrate_roc](./Roc_Auc/CYP2D6-Substrate.PNG) |

### Distribution

## Personal use

### Requirements

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chemprop)](https://badge.fury.io/py/chemprop)
[![PyPI version](https://badge.fury.io/py/chemprop.svg)](https://badge.fury.io/py/chemprop)

To use the provided notebook for chemical prediction and evaluation, you need:

- chemprop >= 1.5.2
- subprocess
- pandas
- numpy
- sklearn
- matplotlib

All the modules can either be installed from `PyPi` via pip or from `source` (i.e., directly from the git repository).

### Data

In order to train a model or obtain predictions, you must provide data containing molecules (as SMILES strings) and known target values.

The data used in this research can be found in the `Datasets` folder.

### Training

You can create a model on your own using [chemprop](https://github.com/chemprop/chemprop/blob/master/README.md#training) module or use publicly available models that are licalted in the `Models` folder.

### Predicting

To load a trained model and make predictions, run all the commands specified in the `Chemical Property Prediction and Evaluation.ipynb` file.
