# Supplementary Methods - Computational Analysis

**Supplementary Material for: [Paper Title]**

This document provides detailed computational methods corresponding to the analysis described in our manuscript.

## Overview

This repository contains the complete code implementation of the machine learning pipeline used to predict ecDNA presence in cancer samples. All code corresponds directly to the methods described in our manuscript.

## Data Sources and Processing

### Input Data

**PCAWG Whole Genome Sequencing (WGS) Data:**
- Copy number variation signatures (CNV48)
- Single base substitution signatures (SBS96)
- Insertion/deletion signatures
- Sample metadata with clinical annotations

**TCGA Whole Exome Sequencing (WES) Data:**
- Pan-cancer copy number signatures
- WES 96 mutational signatures
- WES indel signatures

### Data Processing Pipeline

As described in the Methods section of our manuscript:

1. **Sample ID Alignment** (`src/data_processing.py`, lines 20-75)
   - Extraction of specimen IDs from full identifiers
   - Mapping between ICGC and TCGA ID systems
   - Identification of common samples across datasets

2. **Data Merging** (`src/data_processing.py`, lines 77-150)
   - Inner join on specimen IDs
   - Removal of duplicates
   - Filtering of overlapping samples between WGS and WES

3. **Label Assignment** (`src/data_processing.py`, lines 152-180)
   - Binary classification: ecDNA present (1) vs. absent (0)
   - Based on AmpliconArchitect classifications

## Feature Engineering

As described in Supplementary Methods:

### Feature Categorization

Features were categorized into three mutational signature types:

**Training Data** (`src/utils.py`, `categorize_columns_train()`):
- **SBS (Single Base Substitutions)**: Columns containing ':het:', ':LOH:', ':homdel:', or '>'
- **DBS (Doublet Base Substitutions)**: Columns with multiple underscores
- **Indels**: Columns containing 'DEL' or 'INS'

**Test Data** (`src/utils.py`, `categorize_columns_test()`):
- Similar categorization adapted for WES data format

### Normalization

All mutation counts were converted to proportions:

```
proportion_i = count_i / Σ(counts)
```

Implementation: `src/utils.py`, `convert_counts_to_proportions()`

### Feature Naming

Features were renamed sequentially by type (SBS_1, SBS_2, ..., DBS_1, DBS_2, ..., INDELS_1, INDELS_2, ...) for consistency across datasets.

Implementation: `src/utils.py`, `rename_columns_sequentially()`

## Machine Learning Models

### Models Evaluated

All models were implemented using scikit-learn (v0.24+) or respective libraries:

1. **Logistic Regression** - Baseline linear classifier
2. **Random Forest** - 100 estimators, default parameters
3. **Gradient Boosting** - scikit-learn implementation
4. **Decision Tree** - Single tree classifier  
5. **K-Nearest Neighbors** - K=5
6. **Naive Bayes** - Gaussian distribution
7. **XGBoost** - Gradient boosting with optimization
8. **Neural Network** - Custom architecture (see below)

Implementation: `src/model_training.py`, `train_baseline_models()`

### Neural Network Architecture

As described in our Methods:

```
Layer 1: Dense(64 units, ReLU activation, L2 regularization=0.01)
Layer 2: Dense(32 units, ReLU activation, L2 regularization=0.01)
Layer 3: Dense(16 units, ReLU activation, L2 regularization=0.01)
Output:  Dense(1 unit, Sigmoid activation, L2 regularization=0.01)
```

**Training parameters:**
- Optimizer: Adam
- Loss: Binary cross-entropy
- Epochs: 25
- Batch size: 32
- Validation split: 20%

Implementation: `src/model_training.py`, lines 120-155

### Hyperparameter Optimization

**XGBoost Grid Search:**

Parameters tested:
- `n_estimators`: [100, 400, 800]
- `max_depth`: [3, 6, 9]
- `learning_rate`: [0.05, 0.1, 0.20]

**Cross-validation:**
- 10-fold stratified cross-validation
- Metric: Accuracy
- Random state: 42 (for reproducibility)

Implementation: `src/model_training.py`, `hyperparameter_tuning()`

Best parameters selected:
- `n_estimators`: 400
- `max_depth`: 6
- `learning_rate`: 0.2

### Final Model

The final model used a prediction threshold of 0.05 instead of the standard 0.5 to optimize for sensitivity in detecting ecDNA-positive samples.

Implementation: `src/model_training.py`, `final_model_evaluation()`

## Performance Evaluation

### Metrics

All models were evaluated using:
- **Accuracy**: (TP + TN) / Total
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1-Score**: 2 × (Precision × Recall) / (Precision + Recall)
- **ROC-AUC**: Area under receiver operating characteristic curve

### Cross-Validation

- Stratified K-Fold (K=10)
- Preserves class distribution in each fold
- Random state fixed at 42

Implementation: `src/model_training.py`, `evaluate_model_with_cv()`

### Visualization

ROC curves and confusion matrices were generated for each cross-validation fold and for final test set evaluation.

Implementation: `src/model_training.py`, lines 280-320

## Software and Computing Environment

**Platform:** Google Colab (cloud-based Jupyter notebook environment)

**Python Version:** 3.7+

**Key Dependencies:**
- pandas (1.3.0+) - Data manipulation
- numpy (1.21.0+) - Numerical operations
- scikit-learn (0.24.0+) - Machine learning
- xgboost (1.4.0+) - Gradient boosting
- tensorflow (2.6.0+) - Neural networks
- matplotlib (3.3.0+) - Visualization
- seaborn (0.11.0+) - Statistical visualization

See `requirements.txt` for complete list.

## Reproducibility

### Random Seeds

All random processes use seed 42:
- Train/test splits
- Cross-validation folds
- Model initialization
- Neural network weight initialization

### Data Splits

- **Training set**: PCAWG WGS samples
- **Test set**: TCGA WES samples
- No overlap between training and test sets

### Code Availability

Complete source code is available at:
https://github.com/arjunulag/ecDNA-classification

## Computational Resources

Estimated runtime:
- Data loading and processing: ~10 minutes
- Feature engineering: ~5 minutes
- Baseline model training: ~30 minutes
- Neural network training: ~15 minutes
- Hyperparameter tuning (XGBoost): ~2-3 hours
- Final evaluation: ~10 minutes

**Total**: ~3-4 hours on Google Colab free tier

## References to Code

| Method | Implementation |
|--------|---------------|
| Data loading | `src/data_loading.py` |
| Sample alignment | `src/data_processing.py`, lines 20-75 |
| Feature normalization | `src/utils.py`, lines 100-130 |
| Model training | `src/model_training.py`, lines 30-90 |
| Hyperparameter tuning | `src/model_training.py`, lines 150-220 |
| Cross-validation | `src/model_training.py`, lines 250-320 |

## Contact

For questions regarding computational methods:
- Open an issue at https://github.com/arjunulag/ecDNA-classification
- Email: [corresponding author email]

---

**Note**: This repository is provided as supplementary material for our publication. The code is made available to ensure transparency and enable reproducibility of our findings.

