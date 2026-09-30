import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_FILE = os.path.join(MODEL_DIR, 'crime_rate_model.pkl')

FEATURE_COLS = [
    'Year', 'Month', 'Population',
    'Previous_Crime_Rate', 'Previous_Year_Crime_Rate', 'Previous_Month_Crime_Rate',
    'Rolling_3M_Avg', 'Rolling_6M_Avg', 'Rolling_12M_Avg'
]

CATEGORICAL_COLS = ['City', 'Area', 'Crime_Type', 'Severity']

def encode_data(df: pd.DataFrame):
    """Encode categorical columns using LabelEncoders and preserve mapping."""
    df_encoded = df.copy()
    encoders = {}
    
    for cat_col in CATEGORICAL_COLS:
        if cat_col in df_encoded.columns:
            le = LabelEncoder()
            df_encoded[f'{cat_col}_Encoded'] = le.fit_transform(df_encoded[cat_col].astype(str))
            encoders[cat_col] = le
        else:
            df_encoded[f'{cat_col}_Encoded'] = 0
            
    return df_encoded, encoders

def train_and_evaluate_models(df: pd.DataFrame):
    """
    Train Linear Regression and Random Forest Regressor using a time-based train/test split.
    Calculates actual MAE, RMSE, and R2 metrics on test data.
    Saves trained model bundle to models/crime_rate_model.pkl.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    df_encoded, encoders = encode_data(df)
    
    # Feature columns list
    all_feature_cols = [c for c in FEATURE_COLS if c in df_encoded.columns] + \
                       [f'{c}_Encoded' for c in CATEGORICAL_COLS if f'{c}_Encoded' in df_encoded.columns]
    
    target_col = 'Crime_Rate'
    if target_col not in df_encoded.columns:
        if 'Crime_Count' in df_encoded.columns and 'Population' in df_encoded.columns:
            df_encoded['Crime_Rate'] = (df_encoded['Crime_Count'] / df_encoded['Population']) * 100000.0
        else:
            df_encoded['Crime_Rate'] = df_encoded['Crime_Count'].astype(float)
            
    # Chronological sort for time-aware split
    if 'Year' in df_encoded.columns and 'Month' in df_encoded.columns:
        df_encoded = df_encoded.sort_values(by=['Year', 'Month']).reset_index(drop=True)
        
    X = df_encoded[all_feature_cols].copy()
    y = df_encoded[target_col].copy()
    
    # Check minimum samples
    if len(df_encoded) < 10:
        raise ValueError("Insufficient data records to train machine learning models.")
        
    # Time-based Train / Test Split (80% Train, 20% Test chronologically)
    split_idx = int(len(df_encoded) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    # Model 1: Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    
    lr_metrics = {
        'MAE': round(float(mean_absolute_error(y_test, y_pred_lr)), 2),
        'RMSE': round(float(np.sqrt(mean_squared_error(y_test, y_pred_lr))), 2),
        'R2': round(float(r2_score(y_test, y_pred_lr)), 4)
    }
    
    # Model 2: Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    rf_metrics = {
        'MAE': round(float(mean_absolute_error(y_test, y_pred_rf)), 2),
        'RMSE': round(float(np.sqrt(mean_squared_error(y_test, y_pred_rf))), 2),
        'R2': round(float(r2_score(y_test, y_pred_rf)), 4)
    }
    
    # Feature Importances from Random Forest
    raw_feature_names = [col.replace('_Encoded', '') for col in all_feature_cols]
    importances = pd.DataFrame({
        'Feature': raw_feature_names,
        'Importance': rf_model.feature_importances_
    }).sort_values(by='Importance', ascending=False).reset_index(drop=True)
    importances['Importance'] = importances['Importance'].round(4)
    
    # Save best model bundle
    bundle = {
        'model': rf_model,
        'lr_model': lr_model,
        'encoders': encoders,
        'feature_cols': all_feature_cols,
        'rf_metrics': rf_metrics,
        'lr_metrics': lr_metrics,
        'importances': importances,
        'historical_avg_rate': round(float(y.mean()), 2)
    }
    
    joblib.dump(bundle, MODEL_FILE)
    
    return {
        'rf_metrics': rf_metrics,
        'lr_metrics': lr_metrics,
        'importances': importances,
        'y_test': y_test.values,
        'y_pred_rf': y_pred_rf,
        'y_pred_lr': y_pred_lr,
        'dataset_size': len(df),
        'train_size': len(X_train),
        'test_size': len(X_test)
    }

def load_model_bundle():
    """Load model bundle from disk if it exists, auto-extracting models.zip if needed."""
    if not os.path.exists(MODEL_FILE):
        zip_path = os.path.join(BASE_DIR, 'models.zip')
        if os.path.exists(zip_path):
            try:
                import zipfile
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(BASE_DIR)
            except Exception:
                pass

    if os.path.exists(MODEL_FILE):
        try:
            return joblib.load(MODEL_FILE)
        except Exception:
            return None
    return None

def predict_single(input_dict: dict, model_bundle: dict = None):
    """
    Make a single prediction given input features.
    Returns predicted rate, historical average, percent change, and trend direction.
    """
    if model_bundle is None:
        model_bundle = load_model_bundle()
        
    if model_bundle is None:
        raise ValueError("Model has not been trained yet. Please train the model from the dataset or performance page.")
        
    rf_model = model_bundle['model']
    encoders = model_bundle['encoders']
    feature_cols = model_bundle['feature_cols']
    hist_avg = model_bundle.get('historical_avg_rate', 100.0)
    
    row_data = {}
    
    # Basic features
    for col in FEATURE_COLS:
        row_data[col] = float(input_dict.get(col, 0.0))
        
    # Categorical encodings
    for cat_col in CATEGORICAL_COLS:
        val = str(input_dict.get(cat_col, ''))
        if cat_col in encoders and val in encoders[cat_col].classes_:
            encoded_val = encoders[cat_col].transform([val])[0]
        else:
            encoded_val = 0
        row_data[f'{cat_col}_Encoded'] = encoded_val
        
    df_single = pd.DataFrame([row_data])
    
    # Ensure all feature_cols exist
    for col in feature_cols:
        if col not in df_single.columns:
            df_single[col] = 0.0
            
    X_single = df_single[feature_cols]
    pred_rate = round(float(rf_model.predict(X_single)[0]), 2)
    pred_rate = max(0.0, pred_rate)
    
    diff = pred_rate - hist_avg
    pct_change = round((diff / hist_avg * 100.0) if hist_avg > 0 else 0.0, 1)
    
    if pct_change > 2.0:
        trend = "Increasing"
    elif pct_change < -2.0:
        trend = "Decreasing"
    else:
        trend = "Stable"
        
    return {
        'predicted_rate': pred_rate,
        'historical_avg': hist_avg,
        'pct_change': pct_change,
        'trend': trend,
        'model_name': 'Random Forest Regressor'
    }
