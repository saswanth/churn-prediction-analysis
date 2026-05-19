"""Training script for churn prediction model."""

import sys
from src.data_generator import generate_customer_data, save_data, load_data
from src.preprocessing.preprocessor import prepare_data
from src.models.trainer import ChurnModel


def main():
    """Main training pipeline."""
    print("=" * 60)
    print("CHURN PREDICTION MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    # Step 1: Generate data
    print("\n[1/4] Generating synthetic customer data...")
    df = generate_customer_data(n_samples=1000)
    print(f"✓ Generated {len(df)} customer records")
    print(f"✓ Churn rate: {df['Churn'].mean():.2%}")
    save_data(df)
    
    # Step 2: Prepare data
    print("\n[2/4] Preparing and preprocessing data...")
    X_train, X_test, y_train, y_test, preprocessor = prepare_data(df)
    print(f"✓ Training set: {X_train.shape}")
    print(f"✓ Test set: {X_test.shape}")
    preprocessor.save()
    
    # Step 3: Train model
    print("\n[3/4] Training Random Forest model...")
    model = ChurnModel()
    model.train(X_train, y_train)
    
    # Step 4: Evaluate model
    print("\n[4/4] Evaluating model performance...")
    metrics = model.evaluate(X_test, y_test)
    model.save()
    
    # Feature importance
    print("\n=== Top 10 Most Important Features ===")
    feature_names = list(preprocessor.feature_names)
    importance = model.get_feature_importance(feature_names)
    for i, (feature, importance_score) in enumerate(importance[:10], 1):
        print(f"{i:2d}. {feature:30s} - {importance_score:.4f}")
    
    print("\n" + "=" * 60)
    print("✓ MODEL TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Model saved to: models/churn_model.pkl")
    print(f"Ready for predictions via API!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error during training: {e}")
        sys.exit(1)
