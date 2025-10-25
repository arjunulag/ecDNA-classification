"""
Feature engineering and transformation functions.
"""

import pandas as pd
from src.utils import (
    categorize_columns_train, categorize_columns_test,
    convert_counts_to_proportions, rename_columns_sequentially,
    reorder_renamed_columns_x_test
)


def prepare_train_test_split(df_filtered2, final_dataset):
    """
    Prepare training and test datasets from processed data.
    
    Args:
        df_filtered2 (pd.DataFrame): Filtered PCAWG data
        final_dataset (pd.DataFrame): Final TCGA dataset
        
    Returns:
        tuple: (X_train, y_train, X_test, y_test)
    """
    # Prepare training data
    df_filtered3 = df_filtered2.drop(columns=['icgc_specimen_id'])
    df_filtered3 = df_filtered3.applymap(lambda x: pd.to_numeric(x, errors='coerce'))
    
    df_filtered3.columns = df_filtered3.columns.astype(str)
    df_filtered3.columns = df_filtered3.columns.str.replace(r'[\[\]<>,]', '_', regex=True)
    
    X_train = df_filtered3.drop(columns=['ecDNA_label'])
    y_train = df_filtered3['ecDNA_label']
    
    # Prepare test data
    X_test = final_dataset.drop(columns=['ecDNA_label','sample_x','core_sample','sample_y','sample'])
    y_test = final_dataset['ecDNA_label']
    
    return X_train, y_train, X_test, y_test


def transform_features(X_train, X_test):
    """
    Transform features by converting counts to proportions and renaming columns.
    
    Args:
        X_train (pd.DataFrame): Training features
        X_test (pd.DataFrame): Test features
        
    Returns:
        tuple: (X_train_transformed, X_test_transformed)
    """
    # Process training data
    sbs_train, dbs_train, indels_train = categorize_columns_train(X_train)
    
    X_train = convert_counts_to_proportions(X_train, sbs_train)
    X_train = convert_counts_to_proportions(X_train, dbs_train)
    X_train = convert_counts_to_proportions(X_train, indels_train)
    
    X_train, renamed_sbs_train    = rename_columns_sequentially(X_train, sbs_train, prefix="SBS")
    X_train, renamed_dbs_train    = rename_columns_sequentially(X_train, dbs_train, prefix="DBS")
    X_train, renamed_indels_train = rename_columns_sequentially(X_train, indels_train, prefix="INDELS")
    
    # Process test data
    sbs_test, dbs_test, indels_test = categorize_columns_test(X_test)
    
    X_test = convert_counts_to_proportions(X_test, sbs_test)
    X_test = convert_counts_to_proportions(X_test, dbs_test)
    X_test = convert_counts_to_proportions(X_test, indels_test)
    
    X_test, renamed_sbs_test    = rename_columns_sequentially(X_test, sbs_test, prefix="SBS")
    X_test, renamed_dbs_test    = rename_columns_sequentially(X_test, dbs_test, prefix="DBS")
    X_test, renamed_indels_test = rename_columns_sequentially(X_test, indels_test, prefix="INDELS")
    
    # Reorder test columns
    X_test = reorder_renamed_columns_x_test(X_test)
    
    return X_train, X_test

