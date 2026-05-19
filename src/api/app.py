"""Flask API for churn prediction."""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from src.config import (
    API_HOST, API_PORT, DEBUG, NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES, MODEL_PATH, SCALER_PATH, ENCODER_PATH
)
from src.models.trainer import ChurnModel
from src.preprocessing.preprocessor import ChurnPreprocessor
from src.data_generator import load_data


app = Flask(__name__)
CORS(app)

# Global model and preprocessor
model = None
preprocessor = None


def load_model_and_preprocessor():
    """Load model and preprocessor."""
    global model, preprocessor
    
    try:
        if os.path.exists(MODEL_PATH):
            model = ChurnModel.load(MODEL_PATH)
            preprocessor = ChurnPreprocessor.load(SCALER_PATH, ENCODER_PATH)
            return True
    except Exception as e:
        print(f"Error loading model: {e}")
    
    return False


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict churn for a single customer."""
    if model is None or preprocessor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        
        # Create dataframe from input
        df_input = pd.DataFrame([data])
        
        # Preprocess
        X_processed = preprocessor.transform(df_input)
        
        # Predict
        prediction = model.predict(X_processed)[0]
        probability = model.predict_proba(X_processed)[0]
        
        return jsonify({
            'churn_risk': int(prediction),
            'churn_probability': float(probability[1]),
            'no_churn_probability': float(probability[0])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """Predict churn for multiple customers."""
    if model is None or preprocessor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json.get('customers', [])
        
        # Create dataframe from input
        df_input = pd.DataFrame(data)
        
        # Preprocess
        X_processed = preprocessor.transform(df_input)
        
        # Predict
        predictions = model.predict(X_processed)
        probabilities = model.predict_proba(X_processed)
        
        results = []
        for i, (pred, proba) in enumerate(zip(predictions, probabilities)):
            results.append({
                'customer_id': data[i].get('Customer_ID', f'CUST_{i}'),
                'churn_risk': int(pred),
                'churn_probability': float(proba[1])
            })
        
        return jsonify({'predictions': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/statistics', methods=['GET'])
def statistics():
    """Get dataset and model statistics."""
    try:
        df = load_data()
        
        churn_count = int(df['Churn'].sum())
        total_count = int(len(df))
        churn_rate = float(churn_count / total_count)
        
        stats = {
            'total_customers': total_count,
            'churn_customers': churn_count,
            'churn_rate': churn_rate,
            'average_age': float(df['Age'].mean()),
            'average_tenure': float(df['Tenure'].mean()),
            'average_monthly_charges': float(df['Monthly_Charges'].mean()),
        }
        
        if model and preprocessor:
            stats['model_metrics'] = model.metrics
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    """Get feature importance from the model."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        feature_names = list(NUMERICAL_FEATURES) + list(CATEGORICAL_FEATURES)
        importance_list = model.get_feature_importance(feature_names)
        
        return jsonify({
            'features': [{'name': name, 'importance': float(imp)} for name, imp in importance_list]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/sample-data', methods=['GET'])
def sample_data():
    """Get sample data for UI testing."""
    try:
        df = load_data()
        sample = df.sample(min(10, len(df))).to_dict(orient='records')
        
        return jsonify({
            'samples': sample,
            'features': NUMERICAL_FEATURES + CATEGORICAL_FEATURES
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    print("Loading model and preprocessor...")
    if load_model_and_preprocessor():
        print("Model and preprocessor loaded successfully!")
    else:
        print("Warning: Could not load model. Please train the model first.")
    
    print(f"Starting Flask API on {API_HOST}:{API_PORT}")
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)
