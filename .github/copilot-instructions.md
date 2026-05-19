<!-- Churn Prediction Analysis - VS Code Copilot Instructions -->

# Churn Prediction Analysis Project

This is a comprehensive machine learning project for predicting customer churn with an interactive web dashboard. The project includes data generation, model training, REST API backend, and an interactive frontend dashboard.

## Project Setup Completed

- ✅ Project structure scaffolded
- ✅ Data generation module created
- ✅ ML model training pipeline built
- ✅ Flask API backend implemented
- ✅ Interactive web dashboard UI created
- ✅ All dependencies specified in requirements.txt

## Quick Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate data and train model
python train_model.py

# 3. Start API server (in one terminal)
python -m src.api.app

# 4. Serve frontend (in another terminal)
python -m http.server 8000
# Then open: http://localhost:8000/frontend/
```

## Project Features

- **Data Generation**: Creates synthetic customer data with realistic churn patterns
- **Preprocessing**: Automatic feature scaling and encoding
- **Model Training**: Random Forest classifier with evaluation metrics
- **REST API**: Complete API for predictions and analytics
- **Interactive Dashboard**: Web UI with charts, predictions, and insights

## File Structure

```
├── data/                      # Generated datasets
├── models/                    # Trained models
├── src/
│   ├── api/app.py            # Flask API
│   ├── models/trainer.py     # Model class
│   ├── preprocessing/preprocessor.py
│   ├── config.py             # Configuration
│   └── data_generator.py     # Data generation
├── frontend/
│   ├── index.html            # Dashboard UI
│   ├── style.css             # Styling
│   └── script.js             # Functionality
├── train_model.py            # Training script
└── requirements.txt          # Dependencies
```

## API Endpoints

- `GET /api/health` - Model status
- `POST /api/predict` - Single prediction
- `POST /api/batch-predict` - Batch predictions
- `GET /api/statistics` - Dataset statistics
- `GET /api/feature-importance` - Feature rankings
- `GET /api/sample-data` - Sample data

## Development Notes

- Frontend communicates with API on localhost:5000
- Uses CORS for cross-origin requests
- Model saved as pickle file after training
- Data persisted to CSV for reproducibility
