import pandas as pd
import numpy as np

FEATURE_EXPLANATIONS = {
    'Year': 'The calendar year of observation, helping capture long-term macro trends.',
    'Month': 'The month of observation (1-12), enabling the model to learn seasonal patterns (e.g. summer spikes).',
    'Crime_Count': 'Raw total count of reported crime incidents in the specific location and time window.',
    'Population': 'Total census population of the area used to calculate standardized crime rates.',
    'Previous_Crime_Rate': 'Crime rate from the immediately preceding time period (1-step lag).',
    'Previous_Year_Crime_Rate': 'Crime rate from the exact same month of the previous year (12-step lag) to handle year-over-year seasonality.',
    'Previous_Month_Crime_Rate': 'Crime rate from the previous month, capturing recent short-term momentum.',
    'Rolling_3M_Avg': 'Average crime rate over the past 3 months, smoothing out short-term spikes.',
    'Rolling_6M_Avg': 'Average crime rate over the past 6 months, representing medium-term baseline trend.',
    'Rolling_12M_Avg': 'Average crime rate over the past 12 months, reflecting long-term annual baseline rate.'
}

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate analytical features from historical crime data:
    - Lag features (Previous Crime Rate, Previous Year, Previous Month)
    - Rolling averages (3-Month, 6-Month, 12-Month)
    - Chronological sorting to ensure temporal integrity
    """
    df_feat = df.copy()
    
    # Calculate Crime Rate if not present
    if 'Crime_Rate' not in df_feat.columns:
        if 'Crime_Count' in df_feat.columns and 'Population' in df_feat.columns:
            df_feat['Crime_Rate'] = (df_feat['Crime_Count'] / df_feat['Population']) * 100000.0
        else:
            df_feat['Crime_Rate'] = df_feat['Crime_Count'].astype(float)
            
    # Sort chronologically by Year, Month, City, Area, Crime_Type
    sort_cols = [c for c in ['City', 'Area', 'Crime_Type', 'Year', 'Month'] if c in df_feat.columns]
    df_feat = df_feat.sort_values(by=sort_cols).reset_index(drop=True)
    
    # Define grouping key if location/crime type dimensions exist
    group_cols = [c for c in ['City', 'Area', 'Crime_Type'] if c in df_feat.columns]
    
    if group_cols:
        grouped = df_feat.groupby(group_cols)['Crime_Rate']
        
        # 1-month lag
        df_feat['Previous_Crime_Rate'] = grouped.shift(1)
        df_feat['Previous_Month_Crime_Rate'] = grouped.shift(1)
        
        # 12-month lag (same month previous year)
        df_feat['Previous_Year_Crime_Rate'] = grouped.shift(12)
        
        # Rolling averages (min_periods=1 to preserve data)
        df_feat['Rolling_3M_Avg'] = grouped.transform(lambda x: x.shift(1).rolling(window=3, min_periods=1).mean())
        df_feat['Rolling_6M_Avg'] = grouped.transform(lambda x: x.shift(1).rolling(window=6, min_periods=1).mean())
        df_feat['Rolling_12M_Avg'] = grouped.transform(lambda x: x.shift(1).rolling(window=12, min_periods=1).mean())
    else:
        df_feat['Previous_Crime_Rate'] = df_feat['Crime_Rate'].shift(1)
        df_feat['Previous_Month_Crime_Rate'] = df_feat['Crime_Rate'].shift(1)
        df_feat['Previous_Year_Crime_Rate'] = df_feat['Crime_Rate'].shift(12)
        df_feat['Rolling_3M_Avg'] = df_feat['Crime_Rate'].shift(1).rolling(window=3, min_periods=1).mean()
        df_feat['Rolling_6M_Avg'] = df_feat['Crime_Rate'].shift(1).rolling(window=6, min_periods=1).mean()
        df_feat['Rolling_12M_Avg'] = df_feat['Crime_Rate'].shift(1).rolling(window=12, min_periods=1).mean()

    # Fill initial missing lag values cleanly with current rate or overall mean
    overall_mean = df_feat['Crime_Rate'].mean() if not df_feat['Crime_Rate'].empty else 0.0
    
    for lag_col in ['Previous_Crime_Rate', 'Previous_Month_Crime_Rate', 'Previous_Year_Crime_Rate', 
                    'Rolling_3M_Avg', 'Rolling_6M_Avg', 'Rolling_12M_Avg']:
        df_feat[lag_col] = df_feat[lag_col].fillna(df_feat['Crime_Rate']).fillna(overall_mean).round(2)
        
    return df_feat
