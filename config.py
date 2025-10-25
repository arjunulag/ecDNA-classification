"""
Configuration file for ecDNA classification project.
Contains all file paths and directory configurations.
"""

# Base directories
BASE_DIR = "/content/gdrive/MyDrive/Veritas--Arjun_Ulag/PCAWG_WGS"
TCGA_WES_DIR = '/content/gdrive/MyDrive/Veritas--Arjun_Ulag/TCGA_WES'
MERGE_DIR = '/content/gdrive/MyDrive/Veritas--Arjun_Ulag/Merge'
FINAL_DATA_DIR = '/content/gdrive/MyDrive/Veritas--Arjun_Ulag/Final_Data'

# PCAWG WGS files
FILE_PAN_CNV = f"{BASE_DIR}/PanPCAWG_CNV48.matrix.transposed.tsv"
FILE_METADATA = f"{BASE_DIR}/pcawg_metadata.tsv"
FILE_SBS = f"{BASE_DIR}/WGS_PCAWG.96.csv.transposed.tsv"
FILE_INDELS = f"{BASE_DIR}/WGS_PCAWG.indels.csv.transposed.tsv"

# TCGA WES files
PANCN_SIGS_FILE = f'{TCGA_WES_DIR}/PanCNSigs_TCGA.matrix.tsv'
WES_INDELS_FILE = f'{TCGA_WES_DIR}/WES_TCGA.indels.csv'
WES_96_FILE = f'{TCGA_WES_DIR}/WES_TCGA.96.csv'

# Additional data files
FINAL_MERGED_DATA = f'{MERGE_DIR}/final-merged-data.csv'
PCAWG_SIGNATURES = '/content/gdrive/MyDrive/Veritas--Arjun_Ulag/PCAWG_sigProfiler_SBS_signatures_in_samples.csv'
TCGA_SIGNATURES = '/content/gdrive/MyDrive/Veritas--Arjun_Ulag/TCGA_WES_sigProfiler_SBS_signatures_in_samples.csv'
WGS_FILE = f'{FINAL_DATA_DIR}/WGSonly.tsv'

# Output files
FINAL_OUTPUT_PATH = f'{FINAL_DATA_DIR}/merged_dataset_with_ecDNA_label.tsv'
MODEL_OUTPUT_PATH = 'best_model.pkl'

# Model hyperparameters
HYPERPARAMETER_GRID = {
    'n_estimators': [100, 400, 800],
    'max_depth': [3, 6, 9],
    'learning_rate': [0.05, 0.1, 0.20],
}

# Cross-validation settings
CV_SPLITS = 10
RANDOM_STATE = 42

# Neural network settings
NN_EPOCHS = 25
NN_BATCH_SIZE = 32
NN_VALIDATION_SPLIT = 0.2

# Best model settings (from hyperparameter tuning)
BEST_MODEL_PARAMS = {
    'n_estimators': 400,
    'max_depth': 6,
    'learning_rate': 0.2,
}

# Prediction threshold
PREDICTION_THRESHOLD = 0.05

