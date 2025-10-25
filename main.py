"""
Main execution script for ecDNA classification pipeline.

This script orchestrates the entire machine learning pipeline:
1. Loads data from PCAWG and TCGA sources
2. Processes and merges datasets
3. Engineers features
4. Trains multiple ML models
5. Performs hyperparameter tuning
6. Evaluates final model performance
"""

# Mount Google Drive (for Colab execution)
try:
    from google.colab import drive
    drive.mount('/content/gdrive')
except:
    print("Not running on Google Colab, skipping drive mount")

# Import modules
from src.data_loading import (
    load_pcawg_data, load_tcga_wes_data, 
    load_additional_data, load_final_dataset
)
from src.data_processing import (
    process_pcawg_indices, merge_with_labels,
    process_tcga_wes_data
)
from src.feature_engineering import (
    prepare_train_test_split, transform_features
)
from src.model_training import (
    train_baseline_models, train_neural_network,
    hyperparameter_tuning, train_and_save_best_model,
    evaluate_model_with_cv, final_model_evaluation
)


def main():
    """
    Execute the complete ecDNA classification pipeline.
    """
    print("=" * 80)
    print("ecDNA CLASSIFICATION PIPELINE")
    print("=" * 80)
    
    # ========================================================================
    # STEP 1: Load Data
    # ========================================================================
    print("\n[STEP 1] Loading data...")
    df_pan_cnv, df_metadata, df_sbs, df_indels = load_pcawg_data()
    pancn_sigs, wes_indels, wes_96 = load_tcga_wes_data()
    final, samples, sampels2, wgs_ids = load_additional_data()
    
    # ========================================================================
    # STEP 2: Process PCAWG Data
    # ========================================================================
    print("\n[STEP 2] Processing PCAWG data...")
    df_sbs3, df_indels3, df_cnv3 = process_pcawg_indices(
        df_sbs, df_indels, df_pan_cnv, df_metadata
    )
    
    # ========================================================================
    # STEP 3: Merge with Labels
    # ========================================================================
    print("\n[STEP 3] Merging data with ecDNA labels...")
    df_filtered2 = merge_with_labels(
        df_sbs3, df_indels3, df_cnv3, final, samples, sampels2, df_metadata
    )
    
    # ========================================================================
    # STEP 4: Process TCGA WES Data
    # ========================================================================
    print("\n[STEP 4] Processing TCGA WES data...")
    final_dataset = process_tcga_wes_data(
        pancn_sigs, wes_indels, wes_96, df_metadata, wgs_ids, final
    )
    
    # Reload final dataset
    final_dataset = load_final_dataset()
    if final_dataset is None:
        print("Error: Could not load final dataset")
        return
    
    # ========================================================================
    # STEP 5: Prepare Train/Test Split
    # ========================================================================
    print("\n[STEP 5] Preparing train/test split...")
    X_train, y_train, X_test, y_test = prepare_train_test_split(
        df_filtered2, final_dataset
    )
    
    # ========================================================================
    # STEP 6: Feature Engineering
    # ========================================================================
    print("\n[STEP 6] Engineering features...")
    X_train, X_test = transform_features(X_train, X_test)
    
    print(f"Training set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    print(f"Class distribution in training: {y_train.value_counts()}")
    print(f"Class distribution in test: {y_test.value_counts()}")
    
    # ========================================================================
    # STEP 7: Train Baseline Models
    # ========================================================================
    print("\n[STEP 7] Training baseline models...")
    results_df, results = train_baseline_models(X_train, y_train, X_test, y_test)
    print("\nBaseline Model Results:")
    print(results_df)
    
    # ========================================================================
    # STEP 8: Train Neural Network
    # ========================================================================
    print("\n[STEP 8] Training neural network...")
    results_df, scaler, nn_model, history = train_neural_network(
        X_train, y_train, X_test, y_test, results
    )
    print("\nAll Model Results (including Neural Network):")
    print(results_df)
    
    # ========================================================================
    # STEP 9: Hyperparameter Tuning
    # ========================================================================
    print("\n[STEP 9] Performing hyperparameter tuning...")
    best_params = hyperparameter_tuning(X_train, y_train)
    
    # ========================================================================
    # STEP 10: Train and Save Best Model
    # ========================================================================
    print("\n[STEP 10] Training and saving best model...")
    best_model = train_and_save_best_model(X_train, y_train, best_params)
    print(f"Model saved to best_model.pkl")
    
    # ========================================================================
    # STEP 11: Cross-Validation Evaluation
    # ========================================================================
    print("\n[STEP 11] Evaluating model with cross-validation...")
    mean_accuracy, mean_roc_auc = evaluate_model_with_cv(
        best_model, X_train, y_train
    )
    print(f"Mean CV Accuracy: {mean_accuracy:.4f}")
    print(f"Mean ROC AUC: {mean_roc_auc:.4f}")
    
    # ========================================================================
    # STEP 12: Final Model Evaluation
    # ========================================================================
    print("\n[STEP 12] Final model evaluation on test set...")
    test_accuracy, final_model = final_model_evaluation(
        X_train, y_train, X_test, y_test
    )
    
    # ========================================================================
    # Pipeline Complete
    # ========================================================================
    print("\n" + "=" * 80)
    print("PIPELINE COMPLETE")
    print("=" * 80)
    print(f"Final Test Accuracy: {test_accuracy:.4f}")
    print("Model saved as: best_model.pkl")
    print("=" * 80)


if __name__ == "__main__":
    main()

