# Datasets

Below is a list of the datsets used to train models.

## ADMET

### Absorption

| Target | Unit | Size | Task | Metric | References |
|-|-|-|-|-|-|
| Bioavailability | % | 986 | Binary classification | AUROC | [Tingjun Hou, Falcon-Cano, et al., PharmaInformatic](#bioavailability) |
| Pgp Inibitor | % | 1275 | Binary classification | AUROC | [F, B., et al., Tingjun Hou](#pgp-inibitor) |
| Pgp Substrate | % | 332 | Binary classification | AUROC | [Wang, et al.](#pgp-substrate) |
| Caco-2 | cm/s | 910 | Regression | MAE | [Wang, et al.](#caco-2) |
| Lipophilicity | log-ratio | 4200 | Regression | MAE | [AstraZeneca, Wu, et al.](#lipophilicity) |
| Solubility | log mol/L | 9982 | Regression | MAE | [Sorkun et al.](#solubility) |

### Distribution

| Target | Unit | Size | Task | Metric | References |
|-|-|-|-|-|-|
| BBB | % | 27829 | Binary classification | AUROC | [Meng, et al., Li, et al., Shen, et al.](#bbb) |
| PPBR | % | 2790 | Regression | MAE | [AstraZeneca](#ppbr) |
| VDss | L/kg | 1130 | Regression | Spearman | [Lombardo and Yankang](#vdss) |

### Metabolism

| Target | Unit | Size | Task | Metric | References |
|-|-|-|-|-|-|
| CYP1A2 Inhibitor | % | 13239 | Binary classficiation | AUROC | [PubChem](#cyp1a2-inhibitor) |
| CYP2C9 Inhibitior | % | 12881 | Binary classification | AUPRC | [PubChem](#cyp2c9-inhibitior) |
| CYP2C19 Inhibitor | % | 13427 | Binary classficiation | AUROC | [PubChem](#cyp2c19-inhibitor) |
| CYP2D6 Inhibitior | % | 13898 | Binary classification | AUPRC | [PubChem](#cyp2d6-inhibitior) |
| CYP3A4 Inhibitior | % | 12997 | Binary classification | AUPRC | [PubChem](#cyp3a4-inhibitior) |
| CYP2C9 Substrate | % | 900 | Binary classficiation | AUPRC | [PubChem](#cyp2c9-substrate) |
| CYP2D6 Substrate | % | 941 | Binary classficiation | AUPRC | [Carbon-Mangels, et al., Zertzki, et al.](#cyp2d6-substrate) |
| CYP3A4 Substrate | % | 1149 | Binary classficiation | AUROC | [Carbon-Mangels, et al., Zertzki, et al.](#cyp3a4-substrate) |

### Excretion

| Target | Unit | Size | Task | Metric | References |
|-|-|-|-|-|-|
| Half Life | hr | 667 | Regression | Spearman | [Obach, et al.](#half-life) |
| Clearance Hepatocyte | uL.min-1.(10^6 cells)-1 | 1213 | Regression | Spearman | [AstraZeneca, Li, et al.](#clearance-hepatocyte) |
| Clearance Microsome | mL.min-1.g-1 | 1102 | Regression | Spearman | [AstraZeneca, Li, et al.](#clearance-microsome) |

### Toxicity

| Target | Unit | Size | Task | Metric | References |
|-|-|-|-|-|-|
| LD50 | log(1/(mol/kg)) | 7385 | Regression | MAE | [Zhu, et al.] |

## References

### Bioavailability

1. [Human oral bioavailability database by Tingjun Hou](http://modem.ucsd.edu/adme/databases/databases_bioavailability.htm)
2. [Falcon-Cano G, Molina C, Cabrera-Perez MA (2020) ADME prediction with KNIME: development and validation of a publicly available workflow for the prediction of human oral bioavailability. J Chem Inf Model 60(6):2660–2667](https://pubs.acs.org/doi/10.1021/acs.jcim.0c00019)
3. [Oral Bioavailability by PharmaInformatic](https://www.pharmainformatic.com/html/oral_bioavailability__f__.html)

### Pgp Inibitor

1. [F, B., et al., A novel approach for predicting P-glycoprotein (ABCB1) inhibition using molecular interaction fields. Journal of Medicinal Chemistry, 2011. 54(6): p. 1740-51.](https://pubs.acs.org/doi/10.1021/jm101421d)
2. [P-gp inhibitor database by Tingjun Hou](http://modem.ucsd.edu/adme/databases/databases_Pgp_inhibitor.htm)

### Pgp Substrate

1. [Wang, Z., et al., P-glycoprotein substrate models using support vector machines based on a comprehensive data set. Journal of Chemical Information & Modeling, 2011. 51(6): p. 1447-56.](https://pubs.acs.org/doi/10.1021/ci2001583)

### Caco-2

1. [Wang, NN. et al., ADME Properties Evaluation in Drug Discovery: Prediction of Caco-2 Cell Permeability Using a Combination of NSGA-II and Boosting, Journal of Chemical Information and Modeling 2016 56 (4), 763-773.](https://pubmed.ncbi.nlm.nih.gov/27018227/)

### Lipophilicity

1. [AstraZeneca. Experimental in vitro Dmpk and physicochemical data on a set of publicly disclosed compounds (2016)](https://doi.org/10.6019/chembl3301361)

2. [Wu, Zhenqin, et al. “MoleculeNet: a benchmark for molecular machine learning.” Chemical science 9.2 (2018): 513-530.](https://pubs.rsc.org/--/content/articlehtml/2018/sc/c7sc02664a)

### Solubility

1. [Sorkun, M.C., Khetan, A. & Er, S. AqSolDB, a curated reference set of aqueous solubility and 2D descriptors for a diverse set of compounds. Sci Data 6, 143 (2019).](https://doi.org/10.1038/s41597-019-0151-1)

### BBB

1. [Meng, F., Xi, Y., Huang, J. et al. A curated diverse molecular database of blood-brain barrier permeability with chemical descriptors. Sci Data 8, 289 (2021).](https://doi.org/10.1038/s41597-021-01069-5)
2. [Li, H., et al., Effect of selection of molecular descriptors on the prediction of blood-brain barrier penetrating and nonpenetrating agents by statistical learning methods. Journal of Chemical Information & Modeling, 2005. 45(5): p. 1376-84.](https://pubs.acs.org/doi/10.1021/ci050135u)
3. [Shen, J., et al., Estimation of ADME properties with substructure pattern recognition. Journal of Chemical Information & Modeling, 2010. 50(6): p. 1034-41.](https://pubs.acs.org/doi/10.1021/ci100104j)

### PPBR

1. [AstraZeneca. Experimental in vitro Dmpk and physicochemical data on a set of publicly disclosed compounds (2016)](https://doi.org/10.6019/chembl3301361)

### VDss

1. [Lombardo, Franco, and Yankang Jing. “In silico prediction of volume of distribution in humans. Extensive data set and the exploration of linear and nonlinear methods coupled with molecular interaction fields descriptors.” Journal of Chemical Information and Modeling 56.10 (2016): 2042-2052.](https://pubs.acs.org/doi/abs/10.1021/acs.jcim.6b00044?casa_token=SQhDZjizB08AAAAA:zrP4aW5361rH880nm_vVroPqBxjZU8wy0Yb6a0cM7Qvap1aeLQSo0KS3n79wIW0xa64n3Z3V1-lBaQpN)

### CYP1A2 Inhibitor

1. [PubChem. Cytochrome panel assay with activity outcomes](https://pubchem.ncbi.nlm.nih.gov/bioassay/1851)

### CYP2C9 Inhibitior

1. [PubChem. Cytochrome panel assay with activity outcomes](https://pubchem.ncbi.nlm.nih.gov/bioassay/1851)

### CYP2C19 Inhibitor

1. [PubChem. Cytochrome panel assay with activity outcomes](https://pubchem.ncbi.nlm.nih.gov/bioassay/1851)

### CYP2D6 Inhibitior

1. [PubChem. Cytochrome panel assay with activity outcomes](https://pubchem.ncbi.nlm.nih.gov/bioassay/1851)

### CYP3A4 Inhibitior

1. [PubChem. Cytochrome panel assay with activity outcomes](https://pubchem.ncbi.nlm.nih.gov/bioassay/1851)

### CYP2C9 Substrate

1. [PubChem. Cytochrome panel assay with activity outcomes](https://pubchem.ncbi.nlm.nih.gov/bioassay/1851)

### CYP2D6 Substrate

1. [Carbon-Mangels, M. and M.C. Hutter, Selecting Relevant Descriptors for Classification by Bayesian Estimates: A Comparison with Decision Trees and Support Vector Machines Approaches for Disparate Data Sets. Molecular Informatics, 2011. 30(10): p. 885–895.](https://doi.org/10.1002/minf.201100069)
2. [Zaretzki, J., M. Matlock, and S.J. Swamidass, XenoSite: accurately predicting CYP-mediated sites of metabolism with neural networks. Journal of Chemical Information & Modeling, 2013. 53(12): p. 3373-83.](https://pubs.acs.org/doi/10.1021/ci400518g)

### CYP3A4 Substrate

1. [Carbon-Mangels, M. and M.C. Hutter, Selecting Relevant Descriptors for Classification by Bayesian Estimates: A Comparison with Decision Trees and Support Vector Machines Approaches for Disparate Data Sets. Molecular Informatics, 2011. 30(10): p. 885–895.](https://doi.org/10.1002/minf.201100069)
2. [Zaretzki, J., M. Matlock, and S.J. Swamidass, XenoSite: accurately predicting CYP-mediated sites of metabolism with neural networks. Journal of Chemical Information & Modeling, 2013. 53(12): p. 3373-83.](https://pubs.acs.org/doi/10.1021/ci400518g)

### Half Life

1. [Obach, R. Scott, Franco Lombardo, and Nigel J. Waters. “Trend analysis of a database of intravenous pharmacokinetic parameters in humans for 670 drug compounds.” Drug Metabolism and Disposition 36.7 (2008): 1385-1405.](http://dmd.aspetjournals.org/content/36/7/1385.short?casa_token=9RLY3ZV5uqwAAAAA:j6LPQLnRLDOdzsVkew-nT5eIk9i_6LfkRf6FaBkIS1UKDe7oqP2NmymGeSRsGYigtTQXVHgXyoek)

### Clearance Hepatocyte

1. [AstraZeneca. Experimental in vitro Dmpk and physicochemical data on a set of publicly disclosed compounds (2016)](https://doi.org/10.6019/chembl3301361)
2. [Di, Li, et al. “Mechanistic insights from comparing intrinsic clearance values between human liver microsomes and hepatocytes to guide drug design.” European journal of medicinal chemistry 57 (2012): 441-448.](https://www.sciencedirect.com/science/article/pii/S0223523412003959?casa_token=MNBb1xkUT_YAAAAA:3s1kw30Nlv_tSrXYURqsz4j7it5wswWolxgkAPOg_Ts-FqVv3jLnyUFRQu9rNEdyV2FyyXL0VxI)

### Clearance Microsome

1. [AstraZeneca. Experimental in vitro Dmpk and physicochemical data on a set of publicly disclosed compounds (2016)](https://doi.org/10.6019/chembl3301361)
2. [Di, Li, et al. “Mechanistic insights from comparing intrinsic clearance values between human liver microsomes and hepatocytes to guide drug design.” European journal of medicinal chemistry 57 (2012): 441-448.](https://www.sciencedirect.com/science/article/pii/S0223523412003959?casa_token=MNBb1xkUT_YAAAAA:3s1kw30Nlv_tSrXYURqsz4j7it5wswWolxgkAPOg_Ts-FqVv3jLnyUFRQu9rNEdyV2FyyXL0VxI)

### LD50

1. [Zhu, Hao, et al. “Quantitative structure− activity relationship modeling of rat acute toxicity by oral exposure.” Chemical research in toxicology 22.12 (2009): 1913-1921.](https://pubs.acs.org/doi/abs/10.1021/tx900189p?casa_token=vfBbuxuUCqEAAAAA:YAcI0r4Z3rtlRYP_l5H8OlTfdUh3DVlO6ws_h1NkhpaXH3-NrdI2-s5ghWWJbxfPQw-KhQIAwMi1Di3v)
