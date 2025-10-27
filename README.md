# ecDNA Classification Pipeline - Methods Documentation

**Supplementary Code Repository for Research Publication**

This repository contains the complete computational methods and analysis pipeline used in our research on predicting extrachromosomal DNA (ecDNA) presence in cancer samples. This code documentation serves to ensure transparency and reproducibility of our published findings.

## Purpose

This repository provides:
- **Complete methods documentation** for our research paper
- **Transparency** in our computational approaches
- **Reproducibility** of our analytical pipeline
- **Reference implementation** of the algorithms described in our manuscript

The pipeline uses mutational signatures (SBS, DBS, Indels) and copy number variation data to classify cancer samples based on ecDNA presence, processing data from PCAWG (Pan-Cancer Analysis of Whole Genomes) and TCGA (The Cancer Genome Atlas) datasets.

---

> **📄 Note for Reviewers and Readers:**  
> This repository serves as the **supplementary computational methods** for our research publication. The code documents the exact procedures used in our analysis. While the code can be examined for methodology review, actual execution requires controlled-access genomic data (PCAWG/TCGA).
> 
> See **SUPPLEMENTARY_METHODS.md** for detailed methodology documentation corresponding to our manuscript.

---

## Project Structure

```
.
├── README.md
├── requirements.txt
├── config.py                 # Configuration and file paths
├── main.py                   # Main execution pipeline
├── src/
│   ├── __init__.py
│   ├── data_loading.py       # Data loading functions
│   ├── data_processing.py    # Data preprocessing and merging
│   ├── feature_engineering.py # Feature transformations
│   ├── model_training.py     # Model training and evaluation
│   └── utils.py              # Utility functions
└── notebooks/
    └── ecDNA_analysis.ipynb  # Optional: Jupyter notebook version
```

## Features

- **Data Integration**: Merges WGS and WES datasets from PCAWG and TCGA
- **Feature Engineering**: Converts mutation counts to proportions and standardizes features
- **ML Model**: XGBoost
- **Hyperparameter Optimization**: Grid search with cross-validation for XGBoost
- **Comprehensive Evaluation**: ROC curves, confusion matrices, classification reports

## Requirements

- Python 3.7+
- See `requirements.txt` for package dependencies

## Related Publication

**[Citation to be added upon publication]**

Please cite our paper if you reference this methodology in your work.

## Code Documentation

This repository documents the exact computational methods used in our study. The code is organized into modules corresponding to each major analysis step described in our Methods section:

1. **Data Loading** (`src/data_loading.py`) - How we loaded PCAWG and TCGA datasets
2. **Data Processing** (`src/data_processing.py`) - Sample alignment and merging procedures
3. **Feature Engineering** (`src/feature_engineering.py`) - Signature normalization and transformation
4. **Model Training** (`src/model_training.py`) - Machine learning model implementation and evaluation

## Reproducing Our Analysis

**Note**: This code requires access to controlled-access genomic datasets (PCAWG, TCGA). 

For researchers with appropriate data access:

1. Obtain data access through dbGaP/ICGC DACO
2. Update file paths in `config.py`
3. See `DOCUMENTATION.md` for detailed methods

The complete analytical pipeline as described in our manuscript can be examined in `main.py`.

## Data Requirements

The pipeline expects the following data files:

### PCAWG WGS Data
- `PanPCAWG_CNV48.matrix.transposed.tsv`
- `WGS_PCAWG.96.csv.transposed.tsv`
- `WGS_PCAWG.indels.csv.transposed.tsv`
- `pcawg_metadata.tsv`

### TCGA WES Data
- `PanCNSigs_TCGA.matrix.tsv`
- `WES_TCGA.96.csv`
- `WES_TCGA.indels.csv`

### Additional Files
- `final-merged-data.csv` (ecDNA labels)
- `PCAWG_sigProfiler_SBS_signatures_in_samples.csv`
- `TCGA_WES_sigProfiler_SBS_signatures_in_samples.csv`
- `WGSonly.tsv`

## Methods Summary

Our analysis pipeline includes:

- **7 Machine Learning Models**: Logistic Regression, Random Forest, Gradient Boosting, Decision Tree, K-Nearest Neighbors, Naive Bayes, XGBoost
- **Deep Learning**: Neural Network with TensorFlow/Keras
- **Hyperparameter Optimization**: 10-fold stratified cross-validation with grid search
- **Performance Evaluation**: ROC-AUC, confusion matrices, precision, recall, F1-score

Complete methodology details are available in our manuscript and `DOCUMENTATION.md`.

## Repository Structure

See `PROJECT_STRUCTURE.md` for complete documentation of code organization.

## Computational Requirements

Analysis was performed using:
- Google Colab environment
- Python 3.7+
- Standard machine learning libraries (scikit-learn, XGBoost, TensorFlow)

## Data Availability

The genomic data used in this study are available through:
- **PCAWG**: https://dcc.icgc.org/pcawg (requires ICGC DACO approval)
- **TCGA**: https://www.cancer.gov/tcga (requires dbGaP authorization)

## License

MIT License - This code is provided for transparency and reproducibility purposes.

## Citation

If you use or reference this methodology, please cite our publication:

```
[Full citation to be added upon publication]
```

**Preprint**: [Link to be added]  
**DOI**: [To be added]

## Acknowledgments

This research was conducted using data from the Pan-Cancer Analysis of Whole Genomes (PCAWG) and The Cancer Genome Atlas (TCGA) projects.



