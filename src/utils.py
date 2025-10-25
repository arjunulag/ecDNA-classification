"""
Utility functions for data processing and transformations.
"""

import re
import pandas as pd


def get_specimen_id(full_id):
    """
    Extracts the portion after '::'
    
    Args:
        full_id (str): Full identifier string
        
    Returns:
        str: Extracted specimen ID
    """
    return full_id.split("::")[-1]


def clean_sample_ids(df):
    """
    Clean sample IDs by removing prefixes and normalizing case.
    
    Args:
        df (pd.DataFrame): DataFrame with sample IDs in column names
        
    Returns:
        pd.DataFrame: DataFrame with cleaned column names
    """
    df.columns = df.columns.str.replace(r'.*::', '', regex=True)
    df.columns = df.columns.str.lower().str.strip()
    return df


def extract_core_tcga_id(id_string):
    """
    Extract core TCGA ID from full sample identifier.
    
    Args:
        id_string (str): Full TCGA sample identifier
        
    Returns:
        str or None: Core TCGA ID (e.g., 'tcga-xx-0000') or None if no match
    """
    match = re.match(r'(tcga-\w{2}-\d{4})', id_string.lower())
    return match.group(1) if match else None


def generate_indel_encoding(row, columns):
    """
    Generate indel encoding from count data.
    
    Args:
        row (pd.Series): Row of data containing indel counts
        columns (list): List of column names to process
        
    Returns:
        list: List of formatted indel strings
    """
    formatted_indels = []
    for col in columns:
        if ':' in col:
            count = row[col]
            if count > 0:
                parts = col.split(':')
                index = parts[0]
                operation = parts[1]
                base = parts[2] if len(parts) > 2 else "R"
                
                for i in range(count):
                    formatted_indels.append(f"{index}:{operation}:{base}:{i}")
    return formatted_indels


def categorize_columns_train(df):
    """
    Returns three lists of column names for SBS, DBS, Indels in x_train.
    Based on your examples:
      - SBS might include columns containing ':het:', ':LOH:', ':homdel:', or '>'.
      - DBS might include columns with multiple underscores among letters (e.g. 'A_C_A_A').
      - Indels might include columns containing 'DEL' or 'INS' (including 'DEL.', 'INS.', 'DEL_repeats', 'INS_repeats', 'DEL_MH', etc.).
    
    Args:
        df (pd.DataFrame): Training data
        
    Returns:
        tuple: (sbs_cols, dbs_cols, indel_cols) - lists of column names
    """
    sbs_cols = []
    dbs_cols = []
    indel_cols = []
    
    for col in df.columns:
        col_upper = col.upper()
        
        if (':HET:' in col_upper or ':LOH:' in col_upper or ':HOMDEL:' in col_upper or '>' in col):
            sbs_cols.append(col)
        
        elif ('DEL' in col_upper or 'INS' in col_upper):
            indel_cols.append(col)
        
        else:
            if col.count('_') >= 3:
                dbs_cols.append(col)
            else:
                dbs_cols.append(col)
    
    return sbs_cols, dbs_cols, indel_cols


def categorize_columns_test(df):
    """
    Categorize columns for test dataset into SBS, DBS, and Indels.
    
    Args:
        df (pd.DataFrame): Test data
        
    Returns:
        tuple: (dbs_cols, indel_cols, sbs_cols) - lists of column names
    """
    dbs_cols   = []
    indel_cols = []
    sbs_cols   = []
    
    for col in df.columns:
        col_upper = col.upper()
        
        if ('DEL' in col_upper) or ('INS' in col_upper):
            indel_cols.append(col)
        
        elif ('>' in col) and ('_' in col):
            dbs_cols.append(col)
        
        elif (':HET:' in col_upper or ':LOH:' in col_upper or ':HOMDEL:' in col_upper or '>' in col):
            sbs_cols.append(col)
        
        else:
            sbs_cols.append(col)
    
    dbs_cols.sort()
    indel_cols.sort()
    sbs_cols.sort()
    
    return dbs_cols, indel_cols, sbs_cols


def convert_counts_to_proportions(df, col_list):
    """
    Convert count data to proportions by dividing by row sums.
    
    Args:
        df (pd.DataFrame): DataFrame with count data
        col_list (list): List of columns to convert
        
    Returns:
        pd.DataFrame: DataFrame with proportions
    """
    if not col_list:
        return df 
    df = df.copy()
    row_sums = df[col_list].sum(axis=1)
    row_sums = row_sums.replace({0: 1})
    df[col_list] = df[col_list].div(row_sums, axis=0)
    return df


def rename_columns_sequentially(df, columns, prefix):
    """
    Rename columns sequentially with a given prefix.
    
    Args:
        df (pd.DataFrame): DataFrame to modify
        columns (list): List of columns to rename
        prefix (str): Prefix for new column names
        
    Returns:
        tuple: (df, updated_names) - Modified DataFrame and list of new names
    """
    if not columns:
        return df, []
    
    df = df.copy()
    columns_sorted = sorted(columns)
    rename_map = {}
    
    for i, old_col in enumerate(columns_sorted, start=1):
        new_col = f"{prefix}_{i}"
        rename_map[old_col] = new_col
    
    df = df.rename(columns=rename_map)
    updated_names = [rename_map[old] for old in columns_sorted]
    return df, updated_names


def reorder_renamed_columns_x_test(x_test):
    """
    Reorder columns in test set to group by feature type.
    
    Args:
        x_test (pd.DataFrame): Test dataset
        
    Returns:
        pd.DataFrame: Reordered test dataset
    """
    dbs_cols = [col for col in x_test.columns if col.startswith("DBS_")]
    indels_cols = [col for col in x_test.columns if col.startswith("INDELS_")]
    sbs_cols = [col for col in x_test.columns if col.startswith("SBS_")]
    
    other_cols = [
        col for col in x_test.columns
        if not (col.startswith("DBS_") or col.startswith("INDELS_") or col.startswith("SBS_"))
    ]
    
    dbs_cols.sort()
    indels_cols.sort()
    sbs_cols.sort()
    other_cols.sort()
    
    new_order = dbs_cols + indels_cols + sbs_cols + other_cols
    
    x_test_reordered = x_test[new_order]
    
    return x_test_reordered

