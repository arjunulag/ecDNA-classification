"""
Data processing and merging functions.
"""

import pandas as pd
from src.utils import (
    get_specimen_id, clean_sample_ids, extract_core_tcga_id,
    generate_indel_encoding
)
from config import FINAL_OUTPUT_PATH


def process_pcawg_indices(df_sbs, df_indels, df_pan_cnv, df_metadata):
    """
    Process and align PCAWG dataset indices.
    
    Args:
        df_sbs (pd.DataFrame): SBS signatures data
        df_indels (pd.DataFrame): Indels data
        df_pan_cnv (pd.DataFrame): CNV data
        df_metadata (pd.DataFrame): Metadata
        
    Returns:
        tuple: Processed dataframes (df_sbs3, df_indels3, df_cnv3)
    """
    # Extract specimen IDs from SBS and Indels
    df_sbs2 = df_sbs.copy()
    df_sbs2["icgc_specimen_id"] = df_sbs2.index.to_series().apply(get_specimen_id)
    df_sbs2.set_index("icgc_specimen_id", inplace=True, drop=True)
    
    df_indels2 = df_indels.copy()
    df_indels2["icgc_specimen_id"] = df_indels2.index.to_series().apply(get_specimen_id)
    df_indels2.set_index("icgc_specimen_id", inplace=True, drop=True)
    
    print("SBS new shape:", df_sbs2.shape)
    print("Indels new shape:", df_indels2.shape)
    
    # Process metadata
    df_metadata_by_sp = df_metadata.set_index("icgc_specimen_id", drop=False)
    
    # Find common samples
    common_sbs = list(set(df_sbs2.index) & set(df_metadata_by_sp.index))
    common_indels = list(set(df_indels2.index) & set(df_metadata_by_sp.index))
    df_indels2 = df_indels2.loc[common_indels].sort_index()
    df_sbs2 = df_sbs2.loc[common_sbs].sort_index()
    
    # Process CNV data
    cnv_index_example = df_pan_cnv.index[0]
    print("Example CNV index:", cnv_index_example)
    
    metadata_index_example = df_metadata.index[0]
    print("Example metadata index:", metadata_index_example)
    
    common_cnv = set(df_pan_cnv.index) & set(df_metadata.index)
    print("Common between CNV and metadata index:", len(common_cnv))
    
    df_pan_cnv2 = df_pan_cnv.loc[list(common_cnv)].copy()
    
    # Create initial merge
    df_merged = pd.concat([df_sbs2, df_indels2, df_pan_cnv2], axis=1, join='inner')
    print("Final merged shape:", df_merged.shape)
    print(df_merged.head(3))
    
    # Map CNV to ICGC specimen IDs
    overlap_sbs_indels = set(df_sbs2.index) & set(df_indels2.index)
    
    common_cnv = set(df_pan_cnv.index) & set(df_metadata.index)
    df_pan_cnv2 = df_pan_cnv.loc[list(common_cnv)].copy()
    
    aliquot_to_icgc = df_metadata["icgc_specimen_id"].to_dict()
    
    df_pan_cnv2["icgc_specimen_id"] = df_pan_cnv2.index.map(aliquot_to_icgc)
    df_pan_cnv2.set_index("icgc_specimen_id", inplace=True, drop=True)
    
    overlap_sbs_cnv = set(df_sbs2.index) & set(df_pan_cnv2.index)
    overlap_indels_cnv = set(df_indels2.index) & set(df_pan_cnv2.index)
    three_way = set(df_sbs2.index) & set(df_indels2.index) & set(df_pan_cnv2.index)
    
    # Find common samples across all datasets
    common_samples = set(df_sbs2.index) & set(df_indels2.index) & set(df_pan_cnv2.index)
    
    df_sbs3    = df_sbs2.loc[list(common_samples)].sort_index()
    df_indels3 = df_indels2.loc[list(common_samples)].sort_index()
    df_cnv3    = df_pan_cnv2.loc[list(common_samples)].sort_index()
    
    # Check for zero columns
    df_merged = pd.concat([df_sbs3, df_indels3, df_cnv3], axis=1)
    
    zero_cols = df_merged.eq(0).all()
    problem_cols = list(zero_cols[zero_cols].index)
    
    if problem_cols:
        print(f"Warning: These columns contain only zeros: {problem_cols}")
    else:
        print("No columns contain only zeros")
    
    return df_sbs3, df_indels3, df_cnv3


def merge_with_labels(df_sbs3, df_indels3, df_cnv3, final, samples, sampels2, df_metadata):
    """
    Merge genomic data with ecDNA labels.
    
    Args:
        df_sbs3 (pd.DataFrame): Processed SBS data
        df_indels3 (pd.DataFrame): Processed Indels data
        df_cnv3 (pd.DataFrame): Processed CNV data
        final (pd.DataFrame): Final data with labels
        samples (pd.DataFrame): PCAWG signatures
        sampels2 (pd.DataFrame): TCGA signatures
        df_metadata (pd.DataFrame): Metadata
        
    Returns:
        pd.DataFrame: Filtered and merged dataset
    """
    # Clean sample names
    sampels2['clean_name'] = sampels2['Sample Names'].str.lower()
    final['clean_name']    = final['Sample.name'].str.lower()
    
    sampels2['clean_name'] = sampels2['clean_name'].str.split('_').str[0]
    final['clean_name']    = final['clean_name'].str.split('_').str[0]
    
    sampels2['clean_name'] = sampels2['clean_name'].str.split('-').str[:7].str.join('-')
    final['clean_name']    = final['clean_name'].str.split('-').str[:7].str.join('-')
    
    common_samples = set(sampels2['clean_name']).intersection(set(final['clean_name']))
    
    samples["Sample Names"] = samples["Sample Names"].str.upper()
    final["suffix"] = final["Suffix"].str.upper()
    
    common_ids = set(samples["Sample Names"]).intersection(set(final["suffix"]))
    
    # Create ecDNA label
    final['ecDNA_label'] = (final['Classification'] == 'ecDNA').astype(int)
    
    df_merged = pd.concat([df_sbs3, df_indels3, df_cnv3], axis=1)
    df_merged2 = df_merged.join(final[['ecDNA_label']], how='inner')
    
    # Create mapping
    map_sp_to_tcga = {}
    
    for idx, row in df_metadata.iterrows():
        sp_id = row["icgc_specimen_id"]
        tcga_id = row["submitted_sample_id"]
        map_sp_to_tcga[sp_id] = tcga_id
    
    example_keys = list(map_sp_to_tcga.keys())[:10]
    for k in example_keys:
        print(k, "->", map_sp_to_tcga[k])
    
    # Strip column whitespace
    final.columns = final.columns.str.strip()
    
    df_merged = df_merged.reset_index()
    
    # Merge with labels
    df_result = pd.merge(df_merged, final[['icgc_specimen_id', 'ecDNA_label']],
                         on='icgc_specimen_id',
                         how='inner')
    
    df_filtered = df_result[df_result['icgc_specimen_id'].isin(common_ids)]
    df_filtered = df_filtered.drop_duplicates(subset='icgc_specimen_id')
    
    print(df_filtered.shape)
    
    ids = df_filtered[['icgc_specimen_id','ecDNA_label']]
    
    # Filter out overlapping samples
    df_metadata.reset_index(inplace=True)
    df_metadata['normalized_sample_id'] = df_metadata['submitted_sample_id'].str.lower()
    
    filtered_df = df_metadata[df_metadata['normalized_sample_id'].isin(common_samples)]
    new_identifier_set = set(filtered_df['icgc_specimen_id.1'])
    
    df_filtered2 = df_filtered[~df_filtered['icgc_specimen_id'].isin(new_identifier_set)]
    
    # Generate indel encoding
    df_filtered2_fixed = df_filtered2.copy()
    df_filtered2_fixed['indel_encoding'] = df_filtered2.apply(
        lambda row: generate_indel_encoding(row, df_filtered2.columns), axis=1
    )
    
    return df_filtered2


def process_tcga_wes_data(pancn_sigs, wes_indels, wes_96, df_metadata, wgs_ids, final):
    """
    Process TCGA WES data and merge with labels.
    
    Args:
        pancn_sigs (pd.DataFrame): PanCN signatures
        wes_indels (pd.DataFrame): WES indels
        wes_96 (pd.DataFrame): WES 96 signatures
        df_metadata (pd.DataFrame): Metadata
        wgs_ids (set): Set of WGS sample IDs
        final (pd.DataFrame): Final data with labels
        
    Returns:
        pd.DataFrame: Final merged dataset with ecDNA labels
    """
    # Clean sample IDs
    pancn_sigs = clean_sample_ids(pancn_sigs)
    wes_indels = clean_sample_ids(wes_indels)
    wes_96 = clean_sample_ids(wes_96)
    
    # Get sample sets
    pancn_sigs_samples = set(pancn_sigs.columns[1:])
    wes_indels_samples = set(wes_indels.columns[4:])
    wes_96_samples = set(wes_96.columns[2:])
    
    common_samples = wgs_ids & pancn_sigs_samples & wes_indels_samples & wes_96_samples
    
    # Create mappings
    sp_to_tcga_mapping = df_metadata.set_index('icgc_specimen_id')['submitted_sample_id'].str.lower().to_dict()
    wgs_ids_tcga = {sp_to_tcga_mapping[sp] for sp in wgs_ids if sp in sp_to_tcga_mapping}
    
    df_metadata['submitted_sample_id_clean'] = (
        df_metadata['submitted_sample_id']
        .str.lower()
        .str.replace('_', '-')
        .str.strip()
    )
    
    sp_to_tcga_mapping_clean = (
        df_metadata.set_index('icgc_specimen_id')['submitted_sample_id_clean']
        .dropna()
        .to_dict()
    )
    
    wgs_ids_tcga = {sp_to_tcga_mapping_clean[sp] for sp in wgs_ids if sp in sp_to_tcga_mapping_clean}
    
    overlap_pancn = set(df_metadata['submitted_sample_id_clean']).intersection(set(pancn_sigs.columns[1:]))
    overlap_wes = set(df_metadata['submitted_sample_id_clean']).intersection(set(wes_indels.columns[4:]))
    
    # Extract core TCGA IDs
    wes_indels_core_ids = {extract_core_tcga_id(col) for col in wes_indels.columns[4:]}
    metadata_core_ids = {extract_core_tcga_id(id_) for id_ in df_metadata['submitted_sample_id_clean']}
    pancn_core_ids = set(pancn_sigs.columns[1:])
    
    common_core_ids = wes_indels_core_ids.intersection(metadata_core_ids, pancn_core_ids)
    
    # Filter datasets
    filtered_pancn_sigs = pancn_sigs[['mutation types'] + [id_ for id_ in pancn_sigs.columns if id_ in common_core_ids]]
    filtered_wes_indels = wes_indels[['type', 'subtype', 'indel_size', 'repeat_mh_size'] + [col for col in wes_indels.columns if extract_core_tcga_id(col) in common_core_ids]]
    filtered_wes_96 = wes_96[['sample'] + [col for col in wes_96.columns if extract_core_tcga_id(col) in common_core_ids]]
    
    filtered_wes_96 = filtered_wes_96.rename(columns={'index': 'sample'}).set_index('sample').reset_index()
    
    # Clean column names
    filtered_wes_indels.columns = ['_'.join(map(str, col)).strip('_') for col in filtered_wes_indels.columns]
    filtered_wes_96.columns = ['_'.join(map(str, col)).strip('_') for col in filtered_wes_96.columns]
    
    filtered_pancn_sigs = filtered_pancn_sigs.rename(columns={filtered_pancn_sigs.columns[0]: 'sample'})
    filtered_wes_indels = filtered_wes_indels.rename(columns={filtered_wes_indels.columns[0]: 'sample'})
    filtered_wes_96 = filtered_wes_96.rename(columns={filtered_wes_96.columns[0]: 'sample'})
    
    # Add core sample IDs
    filtered_pancn_sigs['core_sample'] = filtered_pancn_sigs['sample'].map(extract_core_tcga_id)
    filtered_wes_indels['core_sample'] = filtered_wes_indels['sample'].map(extract_core_tcga_id)
    filtered_wes_96['core_sample'] = filtered_wes_96['sample'].map(extract_core_tcga_id)
    
    common_core_ids = set(filtered_pancn_sigs['core_sample'].dropna()).intersection(
        set(filtered_wes_indels['core_sample'].dropna()),
        set(filtered_wes_96['core_sample'].dropna())
    )
    
    filtered_pancn_sigs = filtered_pancn_sigs[filtered_pancn_sigs['core_sample'].isin(common_core_ids)]
    filtered_wes_indels = filtered_wes_indels[filtered_wes_indels['core_sample'].isin(common_core_ids)]
    filtered_wes_96 = filtered_wes_96[filtered_wes_96['core_sample'].isin(common_core_ids)]
    
    # Merge all datasets
    merged_data = filtered_pancn_sigs.merge(
        filtered_wes_indels, on='core_sample', how='inner'
    ).merge(
        filtered_wes_96, on='core_sample', how='inner'
    )
    
    final['core_sample'] = final['Sample.name'].map(extract_core_tcga_id)
    
    final_dataset = merged_data.merge(
        final[['core_sample', 'ecDNA_label']], on='core_sample', how='inner'
    )
    
    # Save to file
    final_dataset.to_csv(FINAL_OUTPUT_PATH, sep='\t', index=False)
    
    return final_dataset

