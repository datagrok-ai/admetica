![Admetica Logo](./adme_logo.png)

# Admetica

This repository is dedicated to advancing pharmaceutical research through cutting-edge ADME (Absorption, Distribution, Metabolism, and Excretion) prediction.

## Table of Contents

- [Purpose](#purpose)
- [Using at Datagrok](#using-at-datagrok)
- [Available Predictive Models](#available-predictive-models)
  - [Absorption](#absorption)
    - [Pgp-Inhibitor](#pgp-inhibitor)
    - [Pgp-Substrate](#pgp-substrate)
    - [F](#f)
  - [Metabolism](#metabolism)
    - [CYP1A2-Inhibitor](#cyp1a2-inhibitor)
    - [CYP3A4-Inhibitor](#cyp3a4-inhibitor)
    - [CYP3A4-Substrate](#cyp3a4-substrate)
    - [CYP2C19-Inhibitor](#cyp2c19-inhibitor)
    - [CYP2C9-Inhibitor](#cyp2c9-inhibitor)
    - [CYP2C9-Substrate](#cyp2c9-substrate)
    - [CYP2D6-Inhibitor](#cyp2d6-inhibitor)
    - [CYP2D6-Substrate](#cyp2d6-substrate)
  - [Distribution](#distribution)
    - [BBB](#bbb)
- [Own use](#own-use)
  - [Requirements](#requirements)
  - [Data](#data)
  - [Training](#training)
  - [Predicting](#predicting)

## Purpose

Our goal is to provide state-of-the-art ADME prediction tools and resources. We are commited to:

- **Efficient Drug Discovery**: Early identification of compounds with favorable pharmacokinetic profiles minimizes late-stage failures and cost implications.

- **Minimum Side Effects**: Early detection of potential toxicity issues prevents adverse effects during clinical trials and post-market use.

- **Streamlined Drug Design**:  Predicting ADMET properties during the drug development process empowers medicinal chemists to optimize candidate molecules for greater success and efficiency.

## Using at DataGrok

DataGrok provides:

- **Cutting-Edge Machine Learning Models:** We provide cutting-edge machine learning models for accurate ADMET property prediction.

- **Unique Data Integration Capability:** Users can integrate their own experimental data. This empowers researchers to customize and refine predictive models to suit their specific research goals

- **Visual Results Interpretation:** Datagrok provides an expanded range of tools and functionalities for enhancing predictions, data analysis, and results visualization. It is helpful in interpreting the results.

## Available Predictive Models

### Absorption

Absorption is the process by which drugs enter the bloodstream after administration. It is pivotal in pharmaceutical research, enabling enhanced bioavailability, precise dosing, formulation optimization, reduced variability among patient populations, and minimized side effects. In this part, we studied 3 absorption-related endpoints.

#### Pgp-Inhibitor

Pgp-inihibitor is...

The Pgp-Inhibitor dataset combines data from two sources, comprising 1,275 compounds, with 666 classified as inhibitors and 609 as non-inhibitors.

#### Pgp-Substrate

Pgp-Substrate is...

The Pgp-Substrate dataset is derived from a single source, encompassing 332 compounds, of which 126 are substrates, and 206 are non-substrates.

#### F

Bioavailability is...

The range of bioavailability value is 0-100. One threshold (30%) was applied in order to split compounds into posititve and negative. Overall, the dataset contains 986 compounds, where positive category contains 660 compounds and negative 326.

### Metabolism

Metabolism is the intricate biochemical system responsible for managing energy and molecular processes within living organisms. It consists of two essential components: anabolism, where complex molecules are built, requiring energy like an investment, and catabolism, which breaks down substances to release energy, akin to a controlled chemical breakdown. This highly regulated process is influenced by various factors such as genetics, age, and lifestyle choices, impacting energy utilization, growth, repair, and overall vitality in a formal and simplified overview.

#### CYP1A2 Inhibitor

It is...

The CYP1A2 Inhibitor dataset comprises 13,239 compounds, with 5,997 being inhibitors and 7,242 non-inhibitors, sourced from PubChem AID 1851.
Results on dataset (higher is better).

| Dataset | Size | Specificity | Sensitivity | Accuracy |
| :---: | :---: | :---: | :---: | :---: |
| CYP1A2-Inhibitor | 13,239 | 0.8991 | 0.9563 |  0.925 |

![CYP1A2-Inhibitor](./Roc_Auc/CYP1A2-Inhibitor.PNG)

#### CYP3A4 Inhibitor

It is...

The CYP3A4 Inhibitor dataset consists of 12,997 compounds, including 5,265 inhibitors and 7,732 non-inhibitors, obtained from PubChem AID 1851.
Results on dataset (higher is better).

| Dataset | Size | Specificity | Sensitivity | Accuracy |
| :---: | :---: | :---: | :---: | :---: |
| CYP3A4-Inhibitor | 12,997 | 0.8607 | 0.9492 |  0.896 |

![CYP1A2-Inhibitor](./Roc_Auc/CYP3A4-Inhibitor.PNG)

#### CYP3A4 Substrate

It is...

The CYP3A4 Substrate dataset encompasses 1,149 compounds, with 832 being substrates and 317 non-substrates, sourced from two different resources.

#### CYP2C19 Inhibitor

It is...

The CYP2C19 Inhibitor dataset contains 13,427 compounds, featuring 5,905 inhibitors and 7,522 non-inhibitors, obtained from PubChem AID 1851.
Results on dataset (higher is better).

| Dataset | Size | Specificity | Sensitivity | Accuracy |
| :---: | :---: | :---: | :---: | :---: |
| CYP2C19-Inhibitor | 13,427 | 0.8865 | 0.8895 |  0.8879 |

![CYP2C9-Inhibitor](./Roc_Auc/CYP2C19-Inhibitor.PNG)

#### CYP2C9 Inhibitor

It is...

The CYP2C9 Inhibitor dataset comprises 12,881 compounds, including 4,109 inhibitors and 8,772 non-inhibitors, sourced from PubChem AID 1851.
Results on dataset (higher is better).

| Dataset | Size | Specificity | Sensitivity | Accuracy |
| :---: | :---: | :---: | :---: | :---: |
| CYP2C9-Inhibitor | 12,881 | 0.8991 | 0.8797 |  0.8929 |

![CYP2C9-Inhibitor](./Roc_Auc/CYP2C9-Inhibitor.PNG)

#### CYP2C9 Substrate

It is...

The CYP2C9 Substrate dataset contains 899 compounds, with 368 being substrates and 531 non-substrates, obtained from two different resources.

#### CYP2D6 Inhibitor

It is...

The CYP2D6 Inhibitor dataset comprises 13,896 compounds, featuring 2,769 inhibitors and 11,127 non-inhibitors, sourced from PubChem AID 1851.

#### CYP2D6 Substrate

It is...

The CYP2D6 Substrate dataset contains 941 compounds, with 461 being substrates and 480 non-substrates, obtained from two different resources.

### Distribution

#### BBB

It is...

The BBB dataset combines data from three sources, totaling 27,796 compounds, with 8,508 classified as BBB+ and 19,288 as BBB-. This dataset provides valuable insights into blood-brain barrier penetration.

## Own use

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
