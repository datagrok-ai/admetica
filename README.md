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
- [Own use](#own-use)
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

### Metabolism

### Distribution

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
