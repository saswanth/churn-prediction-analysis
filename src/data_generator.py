"""Generate synthetic customer data for churn prediction."""

import pandas as pd
import numpy as np
from pathlib import Path
from src.config import RANDOM_STATE, DATA_DIR


def generate_customer_data(n_samples=1000, seed=RANDOM_STATE):
    """
    Generate synthetic customer dataset.
    
    Args:
        n_samples: Number of customer records to generate
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame with customer data
    """
    np.random.seed(seed)
    
    data = {
        'Customer_ID': [f'CUST_{i:05d}' for i in range(1, n_samples + 1)],
        'Age': np.random.randint(18, 80, n_samples),
        'Tenure': np.random.randint(0, 72, n_samples),  # months
        'Monthly_Charges': np.random.uniform(20, 150, n_samples).round(2),
        'Total_Charges': np.random.uniform(100, 8000, n_samples).round(2),
        'Monthly_Usage_Hours': np.random.randint(0, 720, n_samples),
        'Customer_Support_Contacts': np.random.randint(0, 10, n_samples),
        'Contract_Type': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'Internet_Service': np.random.choice(['Fiber optic', 'DSL', 'No'], n_samples),
        'Payment_Method': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], n_samples),
        'Has_Tech_Support': np.random.choice(['Yes', 'No'], n_samples),
        'Has_Online_Backup': np.random.choice(['Yes', 'No'], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate churn based on patterns
    churn_probability = (
        (df['Tenure'] < 6) * 0.3 +  # New customers more likely to churn
        (df['Monthly_Charges'] > 100) * 0.15 +  # High cost correlation
        (df['Customer_Support_Contacts'] > 5) * 0.2 +  # Support contacts indicate issues
        (df['Contract_Type'] == 'Month-to-month') * 0.15 +  # Month-to-month less committed
        (df['Internet_Service'] == 'Fiber optic') * -0.05  # Fiber optic customers more satisfied
    )
    
    # Clip probabilities and add random noise
    churn_probability = np.clip(churn_probability, 0, 1)
    churn_probability += np.random.normal(0, 0.05, n_samples)
    churn_probability = np.clip(churn_probability, 0, 1)
    
    df['Churn'] = (churn_probability > 0.4).astype(int)
    
    return df


def save_data(df, filename='customers.csv'):
    """Save dataframe to CSV file."""
    filepath = DATA_DIR / filename
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")
    return filepath


def load_data(filename='customers.csv'):
    """Load data from CSV file."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        df = pd.read_csv(filepath)
        # Ensure Churn column is numeric
        df['Churn'] = pd.to_numeric(df['Churn'], errors='coerce')
        return df
    raise FileNotFoundError(f"Data file not found: {filepath}")


if __name__ == "__main__":
    print("Generating synthetic customer data...")
    df = generate_customer_data(n_samples=1000)
    print(f"Generated dataset shape: {df.shape}")
    print(f"Churn rate: {df['Churn'].mean():.2%}")
    save_data(df)
