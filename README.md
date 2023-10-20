# Admetica

It is an open-source global effort with collaborators from academia, biotech startups and big pharma.

Our goal is to improve ADMET (Absorption, Distribution, Metabolism, and Excretion) prediction tools.

We welcome everyone with the expertise in the field. If you are interested in collaboration, feel free to reach us:

- **Email**: [oserhiienko@datagrok.ai](mailto:oserhiienko@datagrok.ai)
- **LinkedIn**: [Oleksandra Serhiienko](https://www.linkedin.com/in/oleksandra-serhiienko-674ab6239)

## Table of Contents

- [Goals](#goals)
- [Integration with Datagrok](#integration-with-datagrok)
- [Available predictive models](#available-predictive-models)
  - [Absorption](#absorption)
  - [Metabolism](#metabolism)
- [Usage](#usage)
  - [Install](#install)
  - [Data](#data)
  - [Training](#training)
  - [Predicting](#predicting)
- [References](#references)

## Goals

Our goal is to provide a tool that is:

- **Accurate**: It has higher characteristics compared to other open-source tools such as ADMETLab, Chemprop, QikProp etc.
- **Open-source**: The source code is freely available for anyone to view, use, modify and distribute.
- **With simple API**: It has an easy-to-use interface and can be integrated into various applications and platforms.
- **Reproducible**: You can access data sources, modeling workflow notebooks and models to easily reproduce and verify the entire modeling process.
- **Easily deployable**: It is easy to set up and use.
- **Performant**: It offers a reliable and high-performance solution for datasets of all sizes.

## Integration with Datagrok

Our tool easily works with many platforms and applications. Here's what you can do with it when using Datagrok:

- **Mix your data:** Combine your data with Datagrok's collected experimantal data for customized predictive models.

- **Visualize results:** Use Datagrok tools for better predictions, data analysis and data visualization.

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

## Usage

### Install

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chemprop)](https://badge.fury.io/py/chemprop)
[![Chemprop PyPI version](https://badge.fury.io/py/chemprop.svg)](https://badge.fury.io/py/chemprop)

To install dependencies using [pipenv](https://pipenv.pypa.io/en/latest/) run the following command:
```bash
pipenv install
```
To install dependencies using [pip](https://pip.pypa.io/en/stable/):
```bash
pip install -r requirements.txt
```
To install dependencies using [conda](https://docs.conda.io/en/latest/):
```bash
conda install --file requirements.txt
```

### Data

In order to train a model or obtain predictions, you must provide data containing molecules (as SMILES strings) and known target values.

The data used in this research can be found in the `Datasets` folder.

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
