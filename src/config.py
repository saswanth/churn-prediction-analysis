"""Configuration settings for the Churn Prediction project."""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, MODEL_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Data configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.1

# Model configuration
MODEL_PATH = MODEL_DIR / "churn_model.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"
ENCODER_PATH = MODEL_DIR / "encoder.pkl"

# Feature names
NUMERICAL_FEATURES = [
    'Age', 'Tenure', 'Monthly_Charges', 'Total_Charges',
    'Monthly_Usage_Hours', 'Customer_Support_Contacts'
]

CATEGORICAL_FEATURES = [
    'Contract_Type', 'Internet_Service', 'Payment_Method',
    'Has_Tech_Support', 'Has_Online_Backup'
]

TARGET = 'Churn'

# API configuration
API_HOST = '0.0.0.0'
API_PORT = 5000
DEBUG = True
