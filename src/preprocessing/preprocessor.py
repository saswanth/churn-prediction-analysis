"""Data preprocessing module for churn prediction."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
from src.config import (
    NUMERICAL_FEATURES, CATEGORICAL_FEATURES, TARGET,
    TEST_SIZE, RANDOM_STATE, SCALER_PATH, ENCODER_PATH
)


class ChurnPreprocessor:
    """Preprocess customer data for model training."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.encoders = {}
        self.feature_names = None
    
    def fit(self, df):
        """Fit preprocessor on training data."""
        # Fit scaler on numerical features
        self.scaler.fit(df[NUMERICAL_FEATURES])
        
        # Fit encoders on categorical features
        for feature in CATEGORICAL_FEATURES:
            encoder = LabelEncoder()
            encoder.fit(df[feature])
            self.encoders[feature] = encoder
        
        return self
    
    def transform(self, df):
        """Transform data using fitted preprocessor."""
        df_processed = df.copy()
        
        # Scale numerical features
        df_processed[NUMERICAL_FEATURES] = self.scaler.transform(df[NUMERICAL_FEATURES])
        
        # Encode categorical features
        for feature in CATEGORICAL_FEATURES:
            if feature in self.encoders:
                df_processed[feature] = self.encoders[feature].transform(df[feature])
        
        # Store feature names
        self.feature_names = list(NUMERICAL_FEATURES) + list(CATEGORICAL_FEATURES)
        
        return df_processed[self.feature_names]
    
    def fit_transform(self, df):
        """Fit and transform data."""
        self.fit(df)
        return self.transform(df)
    
    def save(self, scaler_path=SCALER_PATH, encoder_path=ENCODER_PATH):
        """Save preprocessor components."""
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.encoders, encoder_path)
        print(f"Preprocessor saved: scaler to {scaler_path}, encoders to {encoder_path}")
    
    @classmethod
    def load(cls, scaler_path=SCALER_PATH, encoder_path=ENCODER_PATH):
        """Load preprocessor components."""
        preprocessor = cls()
        preprocessor.scaler = joblib.load(scaler_path)
        preprocessor.encoders = joblib.load(encoder_path)
        return preprocessor


def prepare_data(df, test_size=TEST_SIZE, random_state=RANDOM_STATE):
    """
    Prepare data for model training.
    
    Args:
        df: Raw dataframe
        test_size: Test set ratio
        random_state: Random seed
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    # Remove Customer_ID column
    df_model = df.drop('Customer_ID', axis=1)
    
    # Separate features and target
    X = df_model.drop(TARGET, axis=1)
    y = df_model[TARGET]
    
    # Preprocess features
    preprocessor = ChurnPreprocessor()
    X_processed = preprocessor.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return X_train, X_test, y_train, y_test, preprocessor
