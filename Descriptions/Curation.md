# Data Curation

Here we declare the total data curation pipeline to provide consistent modeling development and prediction results. We use the same data curation rules for both training sets and prediction sets as they should be equally curated.
For model development, we explore the experimental background from which the data was obtained, and for prediction, we strongly recommend using the applicability domain of developed models to ensure if they are applicable to studied biochemical problems.

## Common pipeline for data from different sources

The preliminary curation process guarantees that the data from all used sources is compatible with each other and standardized for further model development. We focus on the following steps:
1. Removing data that is not associated with both structural data and property/activity value.
2. Basically, structural information and a value or binary result are sufficient for modeling, but additional fields of data points are preferable to handle when present:
- Source type - a patent, a manuscript, a commercial database with assays - these categories can provide valuable information as they usually study different chemical classes, and the quality and volume of data can vary significantly.
- Value units - there is no hope to get accurate results with different units, fortunately they could be converted in most cases - like mM/L vs mg/L.
- Endpoint type - different endpoints are difficult to mix for a single model development, properties are usually measured as a single endpoint, activities not  - Inh%, IC50, Ki are not even equal endpoints. Experimental conditions are not always present but play a crucial role, values obtained under different experimental conditions may interfere significantly, for example, solubility measured at 20 C or 35 C is different solubility. It is worth knowing and making different assumptions when a dataset is composed of data obtained in different experiments. Depending on the specific task, this field is just useful or crucial.
    >In well-known databases, such fields are standardized:
in PubChem, this information is provided in the following fields - “Panel Name” or “Panel Target”. In ChEMBL, this information is provided in the following fields - “Assay Description” or “Description”, “Assay Organism”, “Assay Cell Type”, “Target ChEMBL ID”, “Target Name”, “Target Organism”. We DO NOT extract this information from manuscripts. Examples:
For antiviral activity, the “Assay description” may contain “Antiviral activity against HIV-1 in CEM cells” and “Inhibition of purified recombinant HIV-1 protease in a fluorogenic assay,” which means that the first experiment was in vivo and the second in vitro. Those two should never be mixed even if the studied endpoint is IC50 or Ki.
All solubility assays in ChEMBL contain an entry with the mentioned organism “Rattus norvegicus” - it is certainly not an appropriate entry for solubility predictive model development. We can also compare entries from “Description” - “Aqueous solubility at pH 7.4” and “Solubility in SGF at pH 1.8,” and they cannot be mixed either as they fit the model for a specific solvent and specific pH level. “Aqueous solubility at pH 7.4” and “Water solubility at pH 7.4” can be mixed.
- In most cases, data is presented as a point measurement, though confidence intervals could also be provided, we eliminate data with wide deviations.
Sometimes data is presented with relations like >=, <, =. Depending on the task, this data can be used or eliminated. For some biological activities and ADMET properties, data is provided for a certain molecular target (like CYPs, hERG etc.). It is best to know if the data is related to a common biological target, its subunit, or a mutant resistant to some action. Try to take it into account.
- For some biological activities and ADMET properties data is provided for a certain molecular target (like CYPs, hERG etc.). It is best to know if data is related to a common biological target, its subunit or a mutant resistant to some action. Try to take it into account.

## Structural Data Curation

One of the most crucial steps is structural data curation. Though we can proceed without it, the absence of structural standardization may lead to undesirable model properties.

Structural curation steps are:

1. Removal of incorrect structures. We use RDKit to define if the structure is valid.
2. Removal of structures with rare elements. If there is no specific obstacle to conserving structures with rare elements, we remove all structures containing:
	>"R  ", "D  "  "He ", "Li ","Be ", "B  ",,
	"Ne ", "Al ", "Si ", "Ar ", "Sc ", "Ti ", "V  ", "Cr ", "Co ",
	"Ni ", "Ga ", "Ge ", "As ", "Se ",
	"Kr ", "Rb ", "Sr ", "Y  ", "Zr ", "Nb ",
	"Mo ", "Tc ", "Ru ", "Rh ", "Pd ", "Ag ", "Cd ",
	"In ", "Sn ", "Sb ", "Te ", "Xe ", "Cs ",
	"Ba ", "La ", "Ce ", "Pr ", "Nd ", "Pm ", "Sm ",
	"Eu ", "Gd ", "Tb ", "Dy ", "Ho ", "Er ", "Tm ",
	"Yb ", "Lu ", "Hf ", "Ta ", "W  ", "Re ", "Os ",
	"Ir ", "Pt ", "Au ", "Hg ", "Tl ", "Pb ", "Bi ",
	"Po ", "At ", "Rn ", "Fr ", "Ra ", "Ac ", "Th ",
	"Pa ", "U  ", "Np ", "Pu ", "Am ", "Cm ", "Bk ",
	"Cf ", "Es ", "Fm ", "Md ", "No ", "Lr ", "Rf ",
	"Db ", "Sg ", "Bh ", "Hs ", "Mt ", "Ds ", "Rg ",
	"Cn ", "Nh ", "Fl ", "Mc ", "Lv ", "Ts ", "Og "
3. Taking the major component: The desired property usually depends on the single structure. Entries in the dataset representing mixtures and salts contain more than one structural component. This can significantly affect generated descriptors/fingerprints - mixtures and single molecules will have different sets of features.
>Depending on the task, it is not always relevant for salts (2 fragments, one of them is the ion of one atom). Salts should be handled by taking the major fragment and following neutralization (removing of charge) for the majority of molecular target associated models (like hERG) and not for properties.
4. Neutralization: For most tasks, we neutralize molecules as their charge will significantly depend on biological/chemical environment.
5. Standardization of structural formulas: Different chemotypes can be represented differently in various chemical notations. We perform standardization to obtain equal descriptors/fingerprints derived from such groups.
6. Equal aromatization: We transform the whole dataset to an equal aromatic or kekule form.
7. Equal normalization: For all macromolecular target activities and for the majority of properties (except pKa), we perform normalization (not to be confused with neutralization or reionization). Normalization conserves the total charge of the molecule.
8. Equal tautomerization: In most cases, the equal tautomeric form of groups should be present in the whole dataset to avoid different descriptors/fingerprints generation. It is legitimized as both forms are usually present in real systems but lead to different descriptors/fingerprints generations.
9. Handling stereo information: We conserve stereo information only when all the data contains it, otherwise we exclude it.
10. Handling hydrogen information: The presence or absence of hydrogens in the structures leads to unequal descriptors/fingerprints generation. We exclude or add explicit hydrogens to all the structures in the dataset depending on the analyzed problem.

## Endpoint Data Curation

Another major stage of curation deals with experimental numerical data. For this, we focus on the following:
1. Removal of incorrectly annotated data/irrelevant data: We remove such data points if they are not specific to the model. For example, if developing a model for SARS-CoV-2 inhibitors, we exclude all entries for SARS-CoV, MERS, or SARS-CoV-2 mutants.
2. Duplicates handling: Mixed datasets often contain several property/activity values for a single structure. We explore the distribution of these entries and exclude outliers. We usually take the median, and for concentration values, the harmonic mean or median of logarithmic transformed values are also accepted.
>For modeling tasks, duplicates are not just equal structures. We compare and search for duplicates of descriptors/fingerprints vectors.
3. Activity cliffs handling: The majority of machine learning approaches use smooth functions as a model. The last are fitted to capture the data, although structures highly similar to others but with a high difference in property/activity can give a strong bias to parameter estimates. We exclude them when there is just a single activity cliff in the subgroup.
4. Normalization of values obtained in different testing systems: When property/activity values are obtained under different experimental conditions, we try to make a transformation considering differences in one of the experimental conditions.
