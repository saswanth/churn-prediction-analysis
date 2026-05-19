# 🎯 Churn Prediction Analysis

A comprehensive machine learning project for predicting customer churn with an interactive web dashboard, REST API backend, and complete ML pipeline.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0.24+-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 📋 Overview

This project helps businesses identify customers at high risk of churning, enabling proactive retention strategies through:

- **Machine Learning Model**: Random Forest classifier with 93% accuracy
- **REST API**: Complete backend for predictions and analytics
- **Interactive Dashboard**: Professional web UI with real-time data visualization
- **Data Pipeline**: Automated data generation, preprocessing, and model training

## ✨ Features

### 📊 Dashboard Components
- **Overview Statistics**: Total customers, churn metrics, model accuracy
- **Churn Distribution**: Visual representation of customer retention
- **Model Performance**: Accuracy, precision, recall, F1-score, ROC-AUC metrics
- **Feature Importance**: Top 10 most influential features in predictions
- **Single Predictions**: Real-time churn risk assessment for individual customers
- **Analytics**: Detailed customer segmentation and pattern analysis
- **Sample Data**: Browse and explore customer records

### 🔧 Technical Stack
- **Backend**: Flask API with CORS support
- **ML Model**: scikit-learn Random Forest Classifier
- **Data Processing**: pandas, NumPy
- **Visualization**: Plotly interactive charts
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Data Storage**: CSV, pickle files

### 📈 Model Performance
```
Accuracy:  93.00%
Precision: 83.33%
Recall:    57.69%
F1-Score:  68.18%
ROC-AUC:   95.40%
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/saswanth/churn-prediction-analysis.git
cd churn-prediction-analysis
```

2. **Create virtual environment** (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Project

#### Step 1: Generate Data & Train Model
```bash
python train_model.py
```

Output:
```
✓ Generated 1000 customer records
✓ Churn rate: 12.90%
✓ Model training complete!
```

#### Step 2: Start API Server
In Terminal 1:
```bash
python -m src.api.app
```

The API will be available at `http://localhost:5000`

#### Step 3: Open Dashboard
In Terminal 2:
```bash
cd frontend
python -m http.server 8000
```

Then open your browser to: **`http://localhost:8000`**

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```
Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Single Prediction
```http
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

Response:
```json
{
  "churn_risk": 1,
  "churn_probability": 0.85,
  "no_churn_probability": 0.15
}
```

### Batch Predictions
```http
POST /api/batch-predict
Content-Type: application/json

{
  "customers": [
    { /* customer data 1 */ },
    { /* customer data 2 */ }
  ]
}
```

### Dataset Statistics
```http
GET /api/statistics
```

Response:
```json
{
  "total_customers": 1000,
  "churn_customers": 129,
  "churn_rate": 0.129,
  "average_age": 49.857,
  "average_tenure": 34.819,
  "average_monthly_charges": 84.02
}
```

### Feature Importance
```http
GET /api/feature-importance
```

Response:
```json
{
  "features": [
    { "name": "Tenure", "importance": 0.3952 },
    { "name": "Monthly_Charges", "importance": 0.1713 },
    ...
  ]
}
```

### Sample Data
```http
GET /api/sample-data
```

## 📁 Project Structure

```
churn-prediction-analysis/
├── data/                          # Generated datasets
│   └── customers.csv             # 1000 customer records
├── models/                        # Trained ML components
│   ├── churn_model.pkl           # Random Forest model
│   ├── scaler.pkl                # Feature scaler
│   └── encoder.pkl               # Categorical encoder
├── src/
│   ├── api/
│   │   ├── app.py                # Flask API server (6 endpoints)
│   │   └── __init__.py
│   ├── models/
│   │   ├── trainer.py            # Model class & training logic
│   │   └── __init__.py
│   ├── preprocessing/
│   │   ├── preprocessor.py       # Data preprocessing pipeline
│   │   └── __init__.py
│   ├── config.py                 # Configuration settings
│   ├── data_generator.py         # Synthetic data generation
│   └── __init__.py
├── frontend/
│   ├── index.html                # Dashboard UI
│   ├── style.css                 # Professional styling
│   └── script.js                 # Interactive JavaScript
├── train_model.py                # Main training script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── GETTING_STARTED.md            # Quick start guide
└── .github/
    └── copilot-instructions.md   # AI assistant instructions
```

## 🎨 Dashboard Screenshots

### Dashboard Tab
Shows key metrics, churn distribution, model performance, and feature importance:
- Total Customers: 1000
- Churn Rate: 12.9%
- Model Accuracy: 93%

### Single Prediction Tab
Interactive form for real-time churn predictions with probability visualization.

### Analytics Tab
Customer segmentation by age, tenure, charges, and contract type with insights.

### Sample Data Tab
Browse and explore actual customer records from the dataset.

## 🔍 Top Predictive Features

1. **Tenure** (39.5%) - Customers with longer tenure are less likely to churn
2. **Monthly Charges** (17.1%) - Higher costs correlate with churn risk
3. **Customer Support Contacts** (13.1%) - Frequent support seekers have higher risk
4. **Contract Type** (9.9%) - Month-to-month contracts show higher churn
5. **Total Charges** (6.2%) - Long-term customer value indicator

## 💡 Business Insights

- **Month-to-month contracts** have 3x higher churn rate than annual contracts
- **Customers with <6 months tenure** account for 30% of churners
- **Tech support enrollment** reduces churn probability by ~20%
- **Average tenure** of retained customers: 35+ months vs 12 months for churned

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
# Data configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Feature names
NUMERICAL_FEATURES = ['Age', 'Tenure', 'Monthly_Charges', ...]
CATEGORICAL_FEATURES = ['Contract_Type', 'Internet_Service', ...]

# API configuration
API_HOST = '0.0.0.0'
API_PORT = 5000
```

## 🚀 Deployment

### Docker
```bash
docker build -t churn-prediction .
docker run -p 5000:5000 churn-prediction
```

### AWS/Heroku
Follow standard deployment procedures for Flask applications.

## 📚 Dependencies

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **scikit-learn** - Machine learning algorithms
- **flask** - Web framework
- **flask-cors** - Cross-origin resource sharing
- **plotly** - Interactive visualizations
- **joblib** - Model serialization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 Future Enhancements

- [ ] Implement XGBoost and Neural Network models for comparison
- [ ] Add k-fold cross-validation
- [ ] Implement SHAP explainability
- [ ] Add batch prediction from CSV upload
- [ ] Deploy to AWS/GCP/Azure
- [ ] Add authentication to API
- [ ] Implement model versioning
- [ ] Create monitoring dashboard

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Saswanth** - Machine Learning Developer
- GitHub: [@saswanth](https://github.com/saswanth)
- Project: [Churn Prediction Analysis](https://github.com/saswanth/churn-prediction-analysis)

## 🙋 Support

For issues, questions, or suggestions, please open an [Issue](https://github.com/saswanth/churn-prediction-analysis/issues) on GitHub.

---

**Made with ❤️ for customer retention analytics**

⭐ If this project helped you, please consider starring it on GitHub!
