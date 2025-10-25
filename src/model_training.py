"""
Model training and evaluation functions.
"""

import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, roc_curve, auc, 
    confusion_matrix, ConfusionMatrixDisplay
)
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.regularizers import l2

from config import (
    HYPERPARAMETER_GRID, CV_SPLITS, RANDOM_STATE,
    NN_EPOCHS, NN_BATCH_SIZE, NN_VALIDATION_SPLIT,
    BEST_MODEL_PARAMS, PREDICTION_THRESHOLD, MODEL_OUTPUT_PATH
)


def train_baseline_models(X_train, y_train, X_test, y_test):
    """
    Train and evaluate multiple baseline models.
    
    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training labels
        X_test (pd.DataFrame): Test features
        y_test (pd.Series): Test labels
        
    Returns:
        pd.DataFrame: Results dataframe with model performance metrics
    """
    models = {
        "Logistic Regression": LogisticRegression(random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
        "Gradient Boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
        "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
        "Naive Bayes": GaussianNB(),
        "XGBoost": XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            objective='binary:logistic',
            use_label_encoder=False,
            random_state=RANDOM_STATE
        )
    }
    
    results = []
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        results.append({
            "Model": name,
            "Accuracy": acc,
            "Precision": report['weighted avg']['precision'],
            "Recall": report['weighted avg']['recall'],
            "F1-Score": report['weighted avg']['f1-score']
        })
    
    results_df = pd.DataFrame(results)
    results_df.sort_values(by="Accuracy", ascending=False, inplace=True)
    
    return results_df, results


def train_neural_network(X_train, y_train, X_test, y_test, results):
    """
    Train and evaluate a neural network model.
    
    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training labels
        X_test (pd.DataFrame): Test features
        y_test (pd.Series): Test labels
        results (list): List to append results to
        
    Returns:
        tuple: (results_df, scaler, model, history)
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],),
              kernel_regularizer=l2(0.01)),
        Dense(32, activation='relu', kernel_regularizer=l2(0.01)),
        Dense(16, activation='relu', kernel_regularizer=l2(0.01)),
        Dense(1, activation='sigmoid', kernel_regularizer=l2(0.01))
    ])
    
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    history = model.fit(X_train_scaled, y_train,
                        validation_split=NN_VALIDATION_SPLIT,
                        epochs=NN_EPOCHS,
                        batch_size=NN_BATCH_SIZE,
                        verbose=1)
    
    y_pred_prob = model.predict(X_test_scaled)
    y_pred = (y_pred_prob > 0.5).astype(int)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    print(f"Neural Network Accuracy: {accuracy:.2f}")
    print(f"Classification Report:\n{classification_report(y_test, y_pred)}")
    
    results.append({
        "Model": "Neural Network",
        "Accuracy": accuracy,
        "Precision": report['weighted avg']['precision'],
        "Recall": report['weighted avg']['recall'],
        "F1-Score": report['weighted avg']['f1-score']
    })
    
    results_df = pd.DataFrame(results)
    results_df.sort_values(by="Accuracy", ascending=False, inplace=True)
    
    return results_df, scaler, model, history


def hyperparameter_tuning(X_train, y_train):
    """
    Perform hyperparameter tuning for XGBoost using cross-validation.
    
    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training labels
        
    Returns:
        dict: Best hyperparameters found
    """
    param_combinations = list((
        HYPERPARAMETER_GRID['n_estimators'],
        HYPERPARAMETER_GRID['max_depth'],
        HYPERPARAMETER_GRID['learning_rate']
    ))
    
    skf = StratifiedKFold(n_splits=CV_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    
    best_score = 0.0
    best_params = {}
    
    for n_estimators, max_depth, learning_rate in param_combinations:
        cv_scores = []
        print(f"Evaluating combination: n_estimators={n_estimators}, max_depth={max_depth}, learning_rate={learning_rate}")
        
        for train_index, test_index in skf.split(X_train, y_train):
            X_fold_train, X_fold_test = X_train.iloc[train_index], X_train.iloc[test_index]
            y_fold_train, y_fold_test = y_train.iloc[train_index], y_train.iloc[test_index]
            
            model = XGBClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                objective='binary:logistic',
                random_state=RANDOM_STATE
            )
            
            model.fit(X_fold_train, y_fold_train)
            y_pred = model.predict(X_fold_test)
            
            acc = accuracy_score(y_fold_test, y_pred)
            cv_scores.append(acc)
        
        mean_cv_score = np.mean(cv_scores)
        print(f"Mean CV Accuracy: {mean_cv_score}\n")
        
        if mean_cv_score > best_score:
            best_score = mean_cv_score
            best_params = {
                'n_estimators': n_estimators,
                'max_depth': max_depth,
                'learning_rate': learning_rate
            }
    
    print("Best Parameters Found:", best_params)
    print("Best Cross-Validation Accuracy:", best_score)
    
    return best_params


def train_and_save_best_model(X_train, y_train, best_params):
    """
    Train the best model with optimal hyperparameters and save it.
    
    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training labels
        best_params (dict): Best hyperparameters
        
    Returns:
        XGBClassifier: Trained model
    """
    best_model = XGBClassifier(
        n_estimators=best_params['n_estimators'],
        max_depth=best_params['max_depth'],
        learning_rate=best_params['learning_rate'],
        objective='binary:logistic',
        random_state=RANDOM_STATE
    )
    
    best_model.fit(X_train, y_train)
    
    with open(MODEL_OUTPUT_PATH, 'wb') as f:
        pickle.dump(best_model, f)
    
    return best_model


def evaluate_model_with_cv(best_model, X_train, y_train):
    """
    Evaluate model using cross-validation with ROC curves and confusion matrices.
    
    Args:
        best_model (XGBClassifier): Trained model
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training labels
        
    Returns:
        tuple: (mean_accuracy, mean_roc_auc)
    """
    skf = StratifiedKFold(n_splits=CV_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    
    accuracies = []
    roc_aucs = []
    
    for train_index, test_index in skf.split(X_train, y_train):
        X_fold_train, X_fold_test = X_train.iloc[train_index], X_train.iloc[test_index]
        y_fold_train, y_fold_test = y_train.iloc[train_index], y_train.iloc[test_index]
        
        best_model.fit(X_fold_train, y_fold_train)
        y_pred_proba = best_model.predict_proba(X_fold_test)[:, 1]
        y_pred = best_model.predict(X_fold_test)
        
        acc = accuracy_score(y_fold_test, y_pred)
        accuracies.append(acc)
        
        cm = confusion_matrix(y_fold_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=best_model.classes_)
        disp.plot(cmap="Blues")
        plt.title("Confusion Matrix")
        plt.show()
        
        fpr, tpr, _ = roc_curve(y_fold_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        roc_aucs.append(roc_auc)
        plt.figure()
        plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC Curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Receiver Operating Characteristic (ROC) Curve")
        plt.legend(loc="lower right")
        plt.show()
    
    mean_accuracy = np.mean(accuracies)
    mean_roc_auc = np.mean(roc_aucs)
    
    return mean_accuracy, mean_roc_auc


def final_model_evaluation(X_train, y_train, X_test, y_test):
    """
    Train final model with best parameters and evaluate on test set.
    
    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training labels
        X_test (pd.DataFrame): Test features
        y_test (pd.Series): Test labels
        
    Returns:
        tuple: (test_accuracy, best_model)
    """
    best_model = XGBClassifier(
        n_estimators=BEST_MODEL_PARAMS['n_estimators'],
        max_depth=BEST_MODEL_PARAMS['max_depth'],
        learning_rate=BEST_MODEL_PARAMS['learning_rate'],
        objective='binary:logistic',
        random_state=RANDOM_STATE,
    )
    best_model.fit(X_train, y_train)
    
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= PREDICTION_THRESHOLD).astype(int)
    
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    cm_test = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm_test, display_labels=best_model.classes_)
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix on Test Data")
    plt.show()
    
    fpr_test, tpr_test, _ = roc_curve(y_test, y_pred_proba)
    roc_auc_test = auc(fpr_test, tpr_test)
    plt.figure()
    plt.plot(fpr_test, tpr_test, color='blue', lw=2, label=f'ROC Curve (AUC = {roc_auc_test:.2f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve on Test Data")
    plt.legend(loc="lower right")
    plt.show()
    
    return test_accuracy, best_model

