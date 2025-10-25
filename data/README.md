# Data Directory

This directory should contain the genomic datasets required for the ecDNA classification pipeline.

## Required Data Files

### PCAWG WGS Data
Place these files in `PCAWG_WGS/` subdirectory:

- **PanPCAWG_CNV48.matrix.transposed.tsv**: Copy number variation signatures
- **WGS_PCAWG.96.csv.transposed.tsv**: Single base substitution (SBS) signatures  
- **WGS_PCAWG.indels.csv.transposed.tsv**: Insertion/deletion signatures
- **pcawg_metadata.tsv**: Sample metadata with IDs and clinical information

### TCGA WES Data
Place these files in `TCGA_WES/` subdirectory:

- **PanCNSigs_TCGA.matrix.tsv**: Pan-cancer copy number signatures
- **WES_TCGA.96.csv**: Whole exome sequencing 96 signatures
- **WES_TCGA.indels.csv**: WES insertion/deletion data

### Additional Files

- **Merge/final-merged-data.csv**: Merged dataset with ecDNA labels
- **PCAWG_sigProfiler_SBS_signatures_in_samples.csv**: PCAWG signature profiles
- **TCGA_WES_sigProfiler_SBS_signatures_in_samples.csv**: TCGA signature profiles
- **Final_Data/WGSonly.tsv**: List of WGS-only sample IDs
- **Final_Data/merged_dataset_with_ecDNA_label.tsv**: Output from processing pipeline

## Directory Structure

```
data/
├── README.md
├── PCAWG_WGS/
│   ├── PanPCAWG_CNV48.matrix.transposed.tsv
│   ├── WGS_PCAWG.96.csv.transposed.tsv
│   ├── WGS_PCAWG.indels.csv.transposed.tsv
│   └── pcawg_metadata.tsv
├── TCGA_WES/
│   ├── PanCNSigs_TCGA.matrix.tsv
│   ├── WES_TCGA.96.csv
│   └── WES_TCGA.indels.csv
├── Merge/
│   └── final-merged-data.csv
└── Final_Data/
    ├── WGSonly.tsv
    └── merged_dataset_with_ecDNA_label.tsv (generated)
```

## Data Sources

- **PCAWG**: Pan-Cancer Analysis of Whole Genomes  
  https://dcc.icgc.org/pcawg

- **TCGA**: The Cancer Genome Atlas  
  https://www.cancer.gov/tcga

## Notes

- Data files are **not** included in the repository due to size and licensing
- You must obtain data from the official sources
- Update paths in `config.py` to match your directory structure
- Some files may be generated during pipeline execution

## File Formats

### TSV/CSV Files
- Tab-separated or comma-separated values
- First row contains column headers
- Sample IDs in first column or as specified

### Matrix Files
- Rows: Samples
- Columns: Features (signatures, mutations, etc.)
- Values: Counts or normalized values

## Data Size

Approximate file sizes:
- CNV matrices: ~100-500 MB
- SBS signatures: ~50-200 MB  
- Indels: ~20-100 MB
- Metadata: ~1-10 MB

**Total**: ~1-2 GB

## Access Requirements

Some datasets may require:
- Data access agreement
- Institutional approval
- dbGaP authorization (for controlled-access data)

Please consult the official data sources for access procedures.

