#Import necessary libraries
import pandas as pd
import numpy as np
import rdkit
from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize
import pubchempy as pcp
import nltk
from nltk import word_tokenize
from collections import Counter
import re

# List where names of columns to be excluded will be stored
columns_to_exclude = []
# Variable to store the smiles column
smiles = ''

def compound_name_to_smiles(compound_name):
    """
    Convert a compound name to canonical SMILES using PubChem.
    
    Parameters:
    - compound_name (str): The name of the compound.
    
    Returns:
    - str or None: The canonical SMILES representation or None if not found.
    """
    try:
        for compound in pcp.get_compounds(compound_name, 'name'):
            return compound.canonical_smiles
    except (IndexError, pcp.PubChemHTTPError):
        return None

def find_columns_with_structures(data):
    """
    Find columns containing chemical structures and perform conversions if needed.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    
    Returns:
    - list: List of columns with chemical structures.
    """
    global smiles  # Declare smiles as a global variable
    
    # Dictionary of conversion functions
    conversion_functions = {
        'smiles_conversion': lambda entry: Chem.MolFromSmiles(entry),
        'molblock_conversion': lambda entry: Chem.MolFromMolBlock(entry),
        'compound_conversion': compound_name_to_smiles
    }

    columns_with_structures = []
    
    for col in data.columns:
        first_valid_index = data[col].first_valid_index() + 1
        first_entry = data[col].loc[first_valid_index]
        
        for conversion_name, conversion_function in conversion_functions.items():
            try:
                if isinstance(first_entry, str) and conversion_function(first_entry):
                    columns_with_structures.append(col)
                    if conversion_name == 'smiles_conversion':
                        smiles = col
                    else:
                        new_col_name = f"{conversion_name}"
                        data[new_col_name] = data[col].apply(conversion_function)
                    break
                if smiles != '':
                    columns_with_structures = []
                    columns_with_structures.append(smiles)
            except:
                pass
    if smiles == '':
        converted_column = [col for col in data.columns if 'molblock_conversion' in col or 'compound_conversion' in col]
        smiles = converted_column[0]
    
    return columns_with_structures

def find_columns_with_sources(data):
    """
    Find columns that potentially contain literature sources.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    
    Returns:
    - list: List of columns with potential literature sources.
    """
    def resembles_url(entry):
        return re.search(r'http[s]?://', entry) is not None
    
    def has_literature_keywords(tokens):
        literature_keywords = ['source', 'reference', 'literature', 'citation']
        return any(keyword in tokens for keyword in literature_keywords)

    potential_source_columns = []
    
    for col in data.columns:
        tokens = [token.lower() for entry in data[col].astype(str) for token in word_tokenize(entry)]
        
        if has_literature_keywords(tokens) or data[col].astype(str).apply(resembles_url).any():
            potential_source_columns.append(col)
            
    return potential_source_columns

def find_columns_with_units(data):
    """
    Find columns containing value units.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    
    Returns:
    - list: List of columns with value units.
    """
    value_units = ["mol/l", "mol/L", "M", "uM", "muM", "nM", "g/L", "g/l", "mg/l", "mg/L", "ug/l", "ug/L"]
    columns_with_units = []
    
    for col in data.columns:
        for value in data[col].astype(str):
            if any(unit.lower() == value.lower() for unit in value_units):
                columns_with_units.append(col)
                break
    
    return columns_with_units

def find_columns_with_endpoint_type(data):
    """
    Find columns related to endpoint types.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    
    Returns:
    - list: List of columns related to endpoint types.
    """
    keywords = ["IC50", "Inhibition", "Ki", "Potency", "Activity", "EC50", "delta pIC50 wt-mutant", "INH", "pIC50", "IP"]
    columns_with_endpoint_type = []
    
    for col in data.columns:
        for value in data[col].astype(str):
            if any(keyword.lower() in value.lower() for keyword in keywords):
                columns_with_endpoint_type.append(col)
                break
    
    return columns_with_endpoint_type

def find_columns_with_conditions(data):
    """
    Find columns related to experimental conditions.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    
    Returns:
    - list: List of columns related to experimental conditions.
    """
    desired_columns = [
        "Panel Name",
        "Panel Target",
        "Assay Description",
        "Description",
        "Assay Organism",
        "Assay Cell Type",
        "Target ChEMBL ID",
        "Target Name",
        "Target Organism"
    ]
    return [col for col in data.columns if col in desired_columns]


def find_columns_with_relations(data):
    """
    Find columns related to relations.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    
    Returns:
    - list: List of columns related to relations.
    """
    relation_columns = []
    relation_pattern = re.compile('[<>=]+')
    
    for col in data.columns:
        if any(relation_pattern.search(str(value)) for value in data[col]) or 'relation' in col.lower():
            relation_columns.append(col)
    
    return relation_columns

def find_binary_columns(data):
    """
    Find columns with data containing only two unique categories or class names.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    
    Returns:
    - list: List of columns with binary data.
    """
    binary_columns = []
    for col in data.columns:
        unique_values = data[col].dropna().unique()
        if len(unique_values) == 2 and 'class' in col.lower():
            binary_columns.append(col)
    return binary_columns

def standardize_molecule(mol):
    # Neutralization
    def neutralize_atoms(mol):
        pattern = Chem.MolFromSmarts("[+1!h0!$([*]~[-1,-2,-3,-4]),-1!$([*]~[+1,+2,+3,+4])]")
        at_matches = mol.GetSubstructMatches(pattern)
        at_matches_list = [y[0] for y in at_matches]
        if len(at_matches_list) > 0:
            for at_idx in at_matches_list:
                atom = mol.GetAtomWithIdx(at_idx)
                chg = atom.GetFormalCharge()
                hcount = atom.GetTotalNumHs()
                atom.SetFormalCharge(0)
                atom.SetNumExplicitHs(hcount - chg)
                atom.UpdatePropertyCache()
        return mol

    mol = neutralize_atoms(mol)

    # Standardization of structural formulas
    mol = rdMolStandardize.Reionize(mol)
    mol = rdMolStandardize.Normalize(mol)

    # Equal tautomerization
    enumerator = rdMolStandardize.TautomerEnumerator()
    mol = enumerator.Canonicalize(mol)

    # Handling stereo information
    def handle_stereochemistry(mol):
        if Chem.MolToSmiles(mol, isomericSmiles=True) != Chem.MolToSmiles(mol, isomericSmiles=False):
            return mol
        else:
            Chem.RemoveStereochemistry(mol)
            return mol

    mol = handle_stereochemistry(mol)

    # Handling hydrogen information
    def handle_hydrogens(mol, exclude=False):
        if exclude:
            Chem.RemoveHs(mol)
        else:
            Chem.AddHs(mol)
        return mol

    mol = handle_hydrogens(mol)

    # Removal structures with rare elements
    elements_to_remove = ["R", "D", "He", "Li", "Be", "B", "Ne", "Al", "Si", "Ar", "Sc", "Ti", "V", "Cr", "Co",
                          "Ni", "Ga", "Ge", "As", "Se", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh",
                          "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm",
                          "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os",
                          "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa",
                          "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg",
                          "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]

    if any(atom.GetSymbol() in elements_to_remove for atom in mol.GetAtoms()):
        return None

    return mol

def process_molecule_data(data, smiles_column):
    """
    Process molecule data in the DataFrame.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    - smiles_column (str): The column containing SMILES representations.
    
    Returns:
    - pd.DataFrame: The processed DataFrame.
    """
    data = data[data[smiles_column].notnull()]
    # Take major component
    data[smiles_column] = data[smiles_column].apply(lambda x: Chem.MolToSmiles(rdMolStandardize.FragmentParent(Chem.MolFromSmiles(x))) if Chem.MolFromSmiles(x) is not None else None)
    data = data[data[smiles_column].notnull()]
    # Create 'Molecule' column
    data['Molecule'] = data[smiles_column].apply(lambda x: Chem.MolFromSmiles(x))
    # Remove invalid structures
    data = data[data['Molecule'].notnull()]

    # Standardize and remove nulls
    data['Molecule'] = data['Molecule'].apply(standardize_molecule)
    data = data[data['Molecule'].notnull()]

    return data


def get_dataset(data):
    """
    Get the final dataset after applying the pipeline.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    
    Returns:
    - pd.DataFrame: The final processed DataFrame.
    """
    columns_to_exclude.extend(find_columns_with_structures(data))
    columns_to_exclude.extend(find_columns_with_sources(data))
    columns_to_exclude.extend(find_columns_with_units(data))
    columns_to_exclude.extend(find_columns_with_endpoint_type(data))
    columns_to_exclude.extend(find_columns_with_conditions(data))
    columns_to_exclude.extend(find_columns_with_relations(data))
    columns_to_exclude.extend(find_binary_columns(data))
    data_final = data[list(set(columns_to_exclude))]
    return data_final


# Read data from CSV file
data = pd.read_csv('HIA.csv')

# Get the final dataset
data_final = get_dataset(data)

# Process molecule data
data_final = process_molecule_data(data_final, smiles)

# Display the final dataset
data_final  