"""Model training module for churn prediction."""

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, roc_curve, classification_report
)
from src.config import MODEL_PATH, RANDOM_STATE


class ChurnModel:
    """Churn prediction model wrapper."""
    
    def __init__(self, random_state=RANDOM_STATE):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=random_state,
            n_jobs=-1
        )
        self.metrics = {}
    
    def train(self, X_train, y_train):
        """Train the model."""
        print("Training model...")
        self.model.fit(X_train, y_train)
        print("Model training complete!")
        return self
    
    def evaluate(self, X_test, y_test):
        """Evaluate model on test set."""
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        print("\n=== Model Evaluation Metrics ===")
        print(f"Accuracy:  {self.metrics['accuracy']:.4f}")
        print(f"Precision: {self.metrics['precision']:.4f}")
        print(f"Recall:    {self.metrics['recall']:.4f}")
        print(f"F1-Score:  {self.metrics['f1']:.4f}")
        print(f"ROC-AUC:   {self.metrics['roc_auc']:.4f}")
        
        return self.metrics
    
    def predict(self, X):
        """Make predictions."""
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get prediction probabilities."""
        return self.model.predict_proba(X)
    
    def get_feature_importance(self, feature_names):
        """Get feature importance scores."""
        importances = self.model.feature_importances_
        return sorted(
            zip(feature_names, importances),
            key=lambda x: x[1],
            reverse=True
        )
    
    def save(self, filepath=MODEL_PATH):
        """Save model to disk."""
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath=MODEL_PATH):
        """Load model from disk."""
        model_obj = cls()
        model_obj.model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")
        return model_obj
