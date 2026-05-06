# ecDNA Classification Pipeline - Methods Documentation

**Supplementary Code Repository for Research Publication**

This repository contains the complete analysis pipeline for predicting extrachromosomal DNA (ecDNA) presence from WES data. 

## Purpose

This repository provides:
- **Complete methods documentation** for our research paper
- **Transparency** in our computational approaches
- **Reproducibility** of our analytical pipeline

The pipeline uses a 227-feature matrix consisting of single-base substitution (SBS96), insertion/deletion (ID83), and copy-number (CN48) features to identify ecDNA-positive samples, using data from the Pan-Cancer Analysis of Whole Genomes (PCAWG) and The Cancer Genome Atlas (TCGA) datasets.

---

> **📄 Note for Reviewers and Readers:**  
> This repository serves as the **supplementary computational methods** for our research publication. The code documents the exact procedures used in our analysis.
> 
> See **SUPPLEMENTARY_METHODS.md** for detailed methodology documentation corresponding to our manuscript.

---

## Feature Matrix

The model uses a 227-feature matrix composed of three mutation-derived feature classes:

- SBS96 single-base substitution contexts
- ID83 insertion/deletion contexts
- CN48 copy-number contexts

Raw count matrices were converted to proportions within each mutation class and then combined into a unified feature matrix for model training and evaluation.

**Copy number feature construction:** Copy number features were derived from WGS-based allele-specific copy number profiles generated using Allele-Specific Copy Number Analysis of Tumors (ASCAT) as part of the PCAWG consensus calls. These copy number profiles were intersected with exonic regions defined by Genome Annotation for the Encyclopedia of DNA Elements (GENCODE), and the resulting exonic-restricted segments were categorized using SigProfilerMatrixGenerator's CN48 schema. The same exonic restriction was applied to SBS96 and ID83 mutation features, ensuring that all feature matrices were derived from WES-accessible genomic regions. ASCAT internally accounts for tumor purity and ploidy estimation. This design tests whether ecDNA-discriminating signal is present within genomic regions accessible to WES, independent of additional noise introduced by native WES-based copy number calling.

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

- **Data Integration**: Loads and aligns WGS-derived and WES-accessible feature data from PCAWG and TCGA sources
- **Feature Engineering**: Constructs a 227-feature matrix from SBS96, ID83, and CN48 mutation-derived features
- **WES-Accessible Feature Design**: Restricts features to genomic signals observable within WES-accessible regions
- **Primary ML Model**: XGBoost
- **Comparator Model**: Feed-forward neural network / multilayer perceptron (MLP)
- **Hyperparameter Optimization**: 3x3 grid search with 10-fold cross-validation for XGBoost
- **Model Evaluation**: Classification accuracy, confusion matrix, and ROC curve

```
  
## Requirements

- Python 3.7+
- See `requirements.txt` for package dependencies

```

## Related Publication

**[Citation to be added upon publication]**

Please cite our paper if you reference this methodology in your work.

## Code Documentation

This repository documents the exact computational methods used in our study. The code is organized into modules corresponding to each major analysis step described in our Methods section:

1. **Data Loading** (`src/data_loading.py`) - How we loaded PCAWG and TCGA datasets
2. **Data Processing** (`src/data_processing.py`) - Sample alignment and merging procedures
3. **Feature Engineering** (`src/feature_engineering.py`) - Signature normalization and transformation
4. **Model Training** (`src/model_training.py`) - Machine learning model implementation and evaluation


The complete analytical pipeline as described in our manuscript can be examined in `main.py`.

## Data Requirements
Input data files are not included in this repository and must be obtained from the appropriate TCGA, PCAWG, and AmpliconRepository data sources. After access and preprocessing, the following processed input files should be placed in the expected input directories:

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

- **Feature Matrix Construction**: SBS96, ID83, and CN48 features combined into a 227-feature matrix
- **Candidate Model Evaluation**: Multiple machine learning classifiers were evaluated during model development, including logistic regression, random forest, gradient boosting, decision tree, k-nearest neighbors, naive Bayes, XGBoost, and neural network models.
- **Primary Reported Model**: XGBoost, which showed the strongest overall performance
- **Comparator Model**: Feed-forward neural network / multilayer perceptron (MLP)
- **Hyperparameter Optimization**: 3x3 grid search with 10-fold cross-validation for XGBoost
- **Model Training and Evaluation**: 5-fold cross-validation, followed by evaluation on the held-out WES test set
- **Performance Evaluation**: Classification Accuracy, confusion matrices, and ROC curves

Complete methodology details are available in our manuscript and `DOCUMENTATION.md`.

## Repository Structure

See `PROJECT_STRUCTURE.md` for complete documentation of code organization.

## Computational Requirements

Analysis was performed using:
- Google Colab environment
- Python 3.7+
- Standard machine learning libraries (scikit-learn, XGBoost, TensorFlow)

## Data Availability

This repository does not redistribute raw genomic data. The analysis used data resources from The Cancer Genome Atlas (TCGA), the Pan-Cancer Analysis of Whole Genomes (PCAWG) project, and AmpliconRepository.

Users should obtain any required data directly from the appropriate data access portals:

- TCGA / GDC Data Portal: https://portal.gdc.cancer.gov/
- PCAWG / ICGC data access: https://docs.icgc-argo.org/docs/data-access/icgc-25k-data
- AmpliconRepository: https://ampliconrepository.org/

Processed input files should be placed in the expected input directories before running the pipeline.

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




