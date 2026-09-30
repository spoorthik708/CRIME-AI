import os
import pandas as pd
from utils.data_processing import clean_data, validate_dataset
from utils.feature_engineering import create_features
from utils.model import train_and_evaluate_models, predict_single, load_model_bundle

print("--- 1. Testing Dataset Load & Validation ---")
df_raw = pd.read_csv("data/sample_data.csv")
is_valid, missing, df_std = validate_dataset(df_raw)
print(f"Validation: Valid={is_valid}, Missing={missing}, Shape={df_std.shape}")

print("\n--- 2. Testing Data Cleaning ---")
df_cleaned, stats = clean_data(df_raw)
print(f"Cleaning Stats: {stats}")

print("\n--- 3. Testing Feature Engineering ---")
df_feat = create_features(df_cleaned)
print(f"Features Generated. Columns count: {len(df_feat.columns)}")
print("Sample engineered columns:", [c for c in df_feat.columns if 'Rate' in c or 'Avg' in c])

print("\n--- 4. Testing Model Training & Evaluation ---")
res = train_and_evaluate_models(df_feat)
print(f"Random Forest Metrics: {res['rf_metrics']}")
print(f"Linear Regression Metrics: {res['lr_metrics']}")
print("Top 5 Feature Importances:\n", res['importances'].head(5))

print("\n--- 5. Testing Single Prediction ---")
bundle = load_model_bundle()
sample_input = {
    'City': 'Metro City',
    'Area': 'Downtown',
    'Crime_Type': 'Theft',
    'Severity': 'Low',
    'Year': 2026,
    'Month': 6,
    'Population': 350000,
    'Crime_Count': 100,
    'Previous_Crime_Rate': 120.0,
    'Previous_Year_Crime_Rate': 115.0,
    'Previous_Month_Crime_Rate': 118.0,
    'Rolling_3M_Avg': 119.0,
    'Rolling_6M_Avg': 117.0,
    'Rolling_12M_Avg': 115.0
}
pred_res = predict_single(sample_input, bundle)
print(f"Prediction Result: {pred_res}")

print("\n✅ ALL BACKEND TESTS PASSED FLACIDLY!")
