# ecDNA Classification - Technical Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Data Pipeline](#data-pipeline)
4. [Feature Engineering](#feature-engineering)
5. [Models](#models)
6. [API Reference](#api-reference)

## Overview

This project implements a machine learning pipeline to predict the presence of extrachromosomal DNA (ecDNA) in cancer samples using mutational signatures and copy number variation data.

### Key Components

- **Data Sources**: PCAWG (WGS) and TCGA (WES) datasets
- **Features**: SBS, DBS, Indels, and CNV signatures
- **Models**: Multiple ML algorithms including XGBoost, Neural Networks, and ensemble methods
- **Output**: Binary classification (ecDNA present/absent)

## Architecture

```
┌─────────────────┐
│  Data Loading   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preprocessing  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Feature Engineer │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Model Training   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Evaluation     │
└─────────────────┘
```

## Data Pipeline

### 1. Data Loading

**PCAWG WGS Data:**
- Copy Number Variations (CNV)
- Single Base Substitutions (SBS)
- Insertions/Deletions (Indels)
- Sample metadata

**TCGA WES Data:**
- PanCN signatures
- WES 96 signatures
- WES indels

### 2. Data Processing

**Index Alignment:**
- Extract specimen IDs from full identifiers
- Map between different ID systems (ICGC ↔ TCGA)
- Find common samples across datasets

**Merging Strategy:**
- Inner join on specimen IDs
- Remove duplicates
- Filter overlapping samples

### 3. Label Assignment

Labels are derived from the `Classification` column in the merged dataset:
- `ecDNA` → Label 1
- Non-ecDNA → Label 0

## Feature Engineering

### Column Categorization

**Training Data:**
- **SBS**: Contains `:het:`, `:LOH:`, `:homdel:`, or `>`
- **DBS**: Contains multiple underscores
- **Indels**: Contains `DEL` or `INS`

**Test Data:**
- Similar categorization with adjusted rules for WES data

### Transformations

1. **Count to Proportion**: Normalize counts by row sums
   ```python
   proportions = counts / row_sum
   ```

2. **Sequential Renaming**: Standardize column names
   ```python
   SBS_1, SBS_2, ..., SBS_N
   DBS_1, DBS_2, ..., DBS_M
   INDELS_1, INDELS_2, ..., INDELS_K
   ```

3. **Column Reordering**: Group features by type for consistency

## Models

### Baseline Models

1. **Logistic Regression**
   - Linear classification baseline
   - Fast training and inference

2. **Random Forest**
   - Ensemble of decision trees
   - 100 estimators

3. **Gradient Boosting**
   - Sequential ensemble method
   - Default sklearn parameters

4. **Decision Tree**
   - Single tree classifier
   - Interpretable results

5. **K-Nearest Neighbors**
   - Instance-based learning
   - K=5 neighbors

6. **Naive Bayes**
   - Probabilistic classifier
   - Gaussian distribution assumption

7. **XGBoost**
   - Optimized gradient boosting
   - Best performing baseline

### Neural Network

**Architecture:**
```
Input Layer (N features)
    ↓
Dense (64 units, ReLU, L2=0.01)
    ↓
Dense (32 units, ReLU, L2=0.01)
    ↓
Dense (16 units, ReLU, L2=0.01)
    ↓
Output (1 unit, Sigmoid)
```

**Training:**
- Optimizer: Adam
- Loss: Binary Crossentropy
- Epochs: 25
- Batch Size: 32
- Validation Split: 20%

### Hyperparameter Tuning

**XGBoost Grid Search:**
- `n_estimators`: [100, 400, 800]
- `max_depth`: [3, 6, 9]
- `learning_rate`: [0.05, 0.1, 0.20]

**Validation:**
- 10-fold Stratified Cross-Validation
- Metric: Accuracy

### Best Model

Final model uses optimized parameters:
- `n_estimators`: 400
- `max_depth`: 6
- `learning_rate`: 0.2
- `prediction_threshold`: 0.05

## API Reference

### Data Loading

```python
from src.data_loading import load_pcawg_data, load_tcga_wes_data

df_pan_cnv, df_metadata, df_sbs, df_indels = load_pcawg_data()
pancn_sigs, wes_indels, wes_96 = load_tcga_wes_data()
```

### Data Processing

```python
from src.data_processing import process_pcawg_indices, merge_with_labels

df_sbs3, df_indels3, df_cnv3 = process_pcawg_indices(
    df_sbs, df_indels, df_pan_cnv, df_metadata
)

df_filtered = merge_with_labels(
    df_sbs3, df_indels3, df_cnv3, final, samples, sampels2, df_metadata
)
```

### Feature Engineering

```python
from src.feature_engineering import prepare_train_test_split, transform_features

X_train, y_train, X_test, y_test = prepare_train_test_split(
    df_filtered, final_dataset
)

X_train, X_test = transform_features(X_train, X_test)
```

### Model Training

```python
from src.model_training import train_baseline_models, hyperparameter_tuning

results_df, results = train_baseline_models(X_train, y_train, X_test, y_test)
best_params = hyperparameter_tuning(X_train, y_train)
```

## Performance Metrics

The pipeline evaluates models using:
- **Accuracy**: Overall correctness
- **Precision**: Positive predictive value
- **Recall**: Sensitivity/True positive rate
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under ROC curve

## File Formats

### Input Files

**CNV Data (.tsv):**
```
Sample_ID    CN1:het:1    CN1:LOH:1    ...
SAMPLE001    0.1          0.2          ...
```

**SBS Data (.tsv):**
```
Signature::Sample_ID    A[C>A]A    A[C>A]C    ...
SBS::SAMPLE001          15         8          ...
```

**Metadata (.tsv):**
```
sample_id    icgc_specimen_id    submitted_sample_id    ...
SAMPLE001    SA123456            TCGA-XX-0000          ...
```

### Output Files

**Model (.pkl):**
- Pickled XGBoost classifier
- Can be loaded for inference

**Predictions:**
- Binary labels (0/1)
- Probability scores

## Configuration

All configuration is centralized in `config.py`:
- File paths
- Model hyperparameters
- Cross-validation settings
- Output paths

To adapt for different environments, modify `config.py` accordingly.

## Troubleshooting

### Common Issues

1. **File Not Found**: Update paths in `config.py`
2. **Memory Error**: Process data in chunks or use smaller subset
3. **Dimension Mismatch**: Ensure train/test features are aligned
4. **Poor Performance**: Try different hyperparameters or feature engineering

### Debug Mode

Enable verbose output by adding print statements in relevant modules.

## References

- PCAWG Consortium: https://dcc.icgc.org/pcawg
- TCGA: https://www.cancer.gov/tcga
- XGBoost Documentation: https://xgboost.readthedocs.io/
- scikit-learn: https://scikit-learn.org/

