"""
Data loading functions for PCAWG and TCGA datasets.
"""

import os
import pandas as pd
from config import (
    FILE_PAN_CNV, FILE_METADATA, FILE_SBS, FILE_INDELS,
    PANCN_SIGS_FILE, WES_INDELS_FILE, WES_96_FILE,
    FINAL_MERGED_DATA, PCAWG_SIGNATURES, TCGA_SIGNATURES,
    WGS_FILE, FINAL_OUTPUT_PATH
)


def load_pcawg_data():
    """
    Load PCAWG WGS data files.
    
    Returns:
        tuple: (df_pan_cnv, df_metadata, df_sbs, df_indels)
    """
    print("Loading PCAWG WGS data...")
    
    df_pan_cnv = pd.read_csv(FILE_PAN_CNV, sep='\t', index_col=0)
    df_metadata = pd.read_csv(FILE_METADATA, sep='\t', index_col=0)
    df_sbs = pd.read_csv(FILE_SBS, sep='\t', index_col=0)
    df_indels = pd.read_csv(FILE_INDELS, sep='\t', index_col=0)
    
    print("=== PanPCAWG_CNV48 ===")
    print("Shape:", df_pan_cnv.shape)
    print(df_pan_cnv.head(), "\n")
    
    print("=== Metadata (pcawg_metadata) ===")
    print("Shape:", df_metadata.shape)
    print(df_metadata.head(), "\n")
    
    print("=== SBS (WGS_PCAWG.96) ===")
    print("Shape:", df_sbs.shape)
    print(df_sbs.head(), "\n")
    
    print("=== Indels (WGS_PCAWG.indels) ===")
    print("Shape:", df_indels.shape)
    print(df_indels.head(), "\n")
    
    return df_pan_cnv, df_metadata, df_sbs, df_indels


def load_tcga_wes_data():
    """
    Load TCGA WES data files.
    
    Returns:
        tuple: (pancn_sigs, wes_indels, wes_96)
    """
    print("Loading TCGA WES data...")
    
    pancn_sigs = pd.read_csv(PANCN_SIGS_FILE, sep='\t')
    wes_indels = pd.read_csv(WES_INDELS_FILE)
    wes_96 = pd.read_csv(WES_96_FILE)
    
    print("PanCNSigs file:")
    print(pancn_sigs.head())
    
    print("\nWES Indels file:")
    print(wes_indels.head())
    
    print("\nWES 96 file:")
    print(wes_96.head())
    
    return pancn_sigs, wes_indels, wes_96


def load_additional_data():
    """
    Load additional data files including labels and signatures.
    
    Returns:
        tuple: (final, samples, sampels2, wgs_ids)
    """
    print("Loading additional data files...")
    
    final = pd.read_csv(FINAL_MERGED_DATA)
    samples = pd.read_csv(PCAWG_SIGNATURES)
    sampels2 = pd.read_csv(TCGA_SIGNATURES)
    wgs_ids = pd.read_csv(WGS_FILE, sep='\t', header=None)
    wgs_ids = set(wgs_ids[0].str.lower().str.strip())
    
    return final, samples, sampels2, wgs_ids


def load_final_dataset():
    """
    Load the final merged dataset with ecDNA labels.
    
    Returns:
        pd.DataFrame or None: Final dataset or None if loading fails
    """
    try:
        final_dataset = pd.read_csv(FINAL_OUTPUT_PATH, sep='\t')
        return final_dataset
    except Exception as e:
        print(f"Error loading final dataset: {str(e)}")
        return None

