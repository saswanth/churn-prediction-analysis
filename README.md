# Churn Prediction Analysis Project

A comprehensive machine learning project for predicting customer churn with an interactive web dashboard.

## 📋 Project Overview

This project implements a complete machine learning pipeline for customer churn prediction, including:

- **Data Generation**: Synthetic customer dataset generation with realistic churn patterns
- **Data Preprocessing**: Feature scaling and encoding for model readiness
- **Model Training**: Random Forest classifier with hyperparameter tuning
- **API Backend**: Flask REST API for predictions and analytics
- **Interactive Dashboard**: Web UI for visualization, prediction, and insights

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda package manager

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "churn prediction"
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Project Structure

```
churn prediction/
├── data/                      # Generated datasets
├── models/                    # Trained models and preprocessors
├── notebooks/                 # Jupyter notebooks for analysis
├── src/
│   ├── api/                   # Flask API application
│   │   └── app.py            # Main API server
│   ├── models/                # Model training modules
│   │   └── trainer.py        # Model class and training
│   ├── preprocessing/         # Data preprocessing
│   │   └── preprocessor.py   # Data transformation
│   ├── config.py             # Configuration settings
│   ├── data_generator.py     # Synthetic data generation
│   └── __init__.py
├── frontend/                  # Web dashboard
│   ├── index.html            # Dashboard HTML
│   ├── style.css             # Styling
│   └── script.js             # Frontend JavaScript
├── train_model.py            # Model training script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🎯 Usage

### Step 1: Generate Data and Train Model

```bash
python train_model.py
```

This will:
- Generate 1,000 synthetic customer records
- Save data to `data/customers.csv`
- Train a Random Forest model
- Save model to `models/churn_model.pkl`
- Display evaluation metrics

### Step 2: Start the API Server

In one terminal:
```bash
python -m src.api.app
```

The API will start on `http://localhost:5000`

### Step 3: Open the Dashboard

Open `frontend/index.html` in your web browser or serve it via a local web server:

```bash
# Python 3
python -m http.server 8000
```

Then navigate to `http://localhost:8000/frontend/`

## 📡 API Endpoints

### Health Check
```
GET /api/health
```
Returns model status.

### Single Prediction
```
POST /api/predict
Content-Type: application/json

{
  "Age": 45,
  "Tenure": 24,
  "Monthly_Charges": 65.50,
  "Total_Charges": 1570,
  "Monthly_Usage_Hours": 300,
  "Customer_Support_Contacts": 2,
  "Contract_Type": "Month-to-month",
  "Internet_Service": "Fiber optic",
  "Payment_Method": "Electronic check",
  "Has_Tech_Support": "Yes",
  "Has_Online_Backup": "Yes"
}
```

Returns churn prediction and probability.

### Batch Predictions
```
POST /api/batch-predict
Content-Type: application/json

{
  "customers": [
    { /* customer data */ },
    { /* customer data */ }
  ]
}
```

### Statistics
```
GET /api/statistics
```
Returns dataset and model statistics.

### Feature Importance
```
GET /api/feature-importance
```
Returns top 10 important features.

### Sample Data
```
GET /api/sample-data
```
Returns sample customer data for UI.

## 🖥️ Dashboard Features

The interactive dashboard includes:

1. **Dashboard Tab**
   - Overview statistics
   - Churn distribution pie chart
   - Model performance metrics
   - Feature importance visualization

2. **Single Prediction Tab**
   - Interactive form to input customer data
   - Real-time churn risk assessment
   - Probability visualization
   - Actionable recommendations

3. **Analytics Tab**
   - Age distribution by churn status
   - Tenure analysis
   - Monthly charges impact
   - Contract type analysis
   - Data-driven insights

4. **Sample Data Tab**
   - View sample customer records
   - Data exploration interface

## 📈 Model Performance

The Random Forest classifier typically achieves:
- **Accuracy**: ~85%
- **Precision**: ~82%
- **Recall**: ~78%
- **F1-Score**: ~80%
- **ROC-AUC**: ~88%

(Actual metrics vary based on data generation randomness)

## 🔧 Configuration

Edit `src/config.py` to customize:
- Data paths
- Feature names
- Model hyperparameters
- API host and port

## 📦 Dependencies

- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning
- **flask**: Web API framework
- **flask-cors**: Cross-origin resource sharing
- **plotly**: Interactive visualizations
- **matplotlib/seaborn**: Data visualization

## 🎓 Learning Resources

This project demonstrates:
- Data preprocessing and feature engineering
- Machine learning model training and evaluation
- REST API development with Flask
- Frontend development with vanilla JavaScript
- Data visualization with Plotly
- Interactive web dashboard design

## 🚨 Troubleshooting

**Model not loading?**
- Run `python train_model.py` first to train and save the model

**API connection errors?**
- Ensure Flask server is running on the correct port
- Check CORS settings in `src/api/app.py`

**Dashboard not loading data?**
- Check browser console for error messages
- Verify API endpoints are accessible
- Ensure model file exists in `models/` directory

## 📝 Next Steps

Enhancements you can implement:
- Add more sophisticated models (XGBoost, Neural Networks)
- Implement k-fold cross-validation
- Add model explainability (SHAP values)
- Create training/testing split visualization
- Add customer segmentation analysis
- Implement model retraining pipeline
- Add authentication to API

## 📄 License

This project is provided as-is for educational purposes.

## 👨‍💻 Author

Created as a comprehensive machine learning demonstration project.

---

**Happy predicting! 🚀**
