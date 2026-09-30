import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    'Year', 'Month', 'City', 'Area', 'Crime_Type', 
    'Crime_Count', 'Population', 'Severity', 'Latitude', 'Longitude'
]

COLUMN_ALIASES = {
    'year': 'Year',
    'yr': 'Year',
    'month': 'Month',
    'mnth': 'Month',
    'city': 'City',
    'town': 'City',
    'area': 'Area',
    'location': 'Area',
    'locality': 'Area',
    'crime_type': 'Crime_Type',
    'crimetype': 'Crime_Type',
    'crime category': 'Crime_Type',
    'crime_category': 'Crime_Type',
    'crime_count': 'Crime_Count',
    'crimecount': 'Crime_Count',
    'incidents': 'Crime_Count',
    'count': 'Crime_Count',
    'population': 'Population',
    'pop': 'Population',
    'severity': 'Severity',
    'severity_level': 'Severity',
    'latitude': 'Latitude',
    'lat': 'Latitude',
    'longitude': 'Longitude',
    'lon': 'Longitude',
    'lng': 'Longitude'
}

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize dataframe column names to handle minor casing and naming variations."""
    df_copy = df.copy()
    new_cols = {}
    for col in df_copy.columns:
        col_clean = str(col).strip().lower().replace(' ', '_')
        if col_clean in COLUMN_ALIASES:
            new_cols[col] = COLUMN_ALIASES[col_clean]
        else:
            # Match without underscores
            col_no_underscore = col_clean.replace('_', '')
            if col_no_underscore in COLUMN_ALIASES:
                new_cols[col] = COLUMN_ALIASES[col_no_underscore]
            else:
                new_cols[col] = col
    df_copy.rename(columns=new_cols, inplace=True)
    return df_copy

def validate_dataset(df: pd.DataFrame):
    """Validate uploaded dataset columns and return missing required columns."""
    df_std = standardize_columns(df)
    missing = [col for col in REQUIRED_COLUMNS if col not in df_std.columns]
    is_valid = len(missing) == 0
    return is_valid, missing, df_std

def calculate_crime_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Crime Rate using standard analytical formula:
    Crime Rate = (Crime Count / Population) * 100,000
    """
    df_copy = df.copy()
    if 'Crime_Count' in df_copy.columns and 'Population' in df_copy.columns:
        # Avoid division by zero
        pop_safe = df_copy['Population'].replace(0, np.nan)
        df_copy['Crime_Rate'] = (df_copy['Crime_Count'] / pop_safe) * 100000.0
        df_copy['Crime_Rate'] = df_copy['Crime_Rate'].fillna(0.0).round(2)
    elif 'Crime_Count' in df_copy.columns:
        # Fallback if population missing
        df_copy['Crime_Rate'] = df_copy['Crime_Count'].astype(float)
    return df_copy

def clean_data(df: pd.DataFrame):
    """
    Perform comprehensive data cleaning:
    - missing value detection
    - duplicate removal
    - invalid year detection
    - invalid crime count detection
    - invalid population detection
    - invalid coordinates detection
    - data type conversion
    - crime-type standardization
    
    Returns cleaned dataframe and a statistics dictionary.
    """
    df_work = standardize_columns(df)
    original_records = len(df_work)
    
    # 1. Duplicates check & removal
    duplicates_count = int(df_work.duplicated().sum())
    df_work = df_work.drop_duplicates()
    
    # 2. Missing values count
    missing_count = int(df_work.isnull().sum().sum())
    
    # Fill or drop essential fields
    df_work = df_work.dropna(subset=['Year', 'Month', 'City', 'Crime_Type'])
    
    invalid_mask = pd.Series(False, index=df_work.index)
    
    # 3. Invalid year detection (<1900 or >2100)
    if 'Year' in df_work.columns:
        df_work['Year'] = pd.to_numeric(df_work['Year'], errors='coerce')
        invalid_mask |= (df_work['Year'] < 1900) | (df_work['Year'] > 2100) | (df_work['Year'].isnull())
        
    if 'Month' in df_work.columns:
        df_work['Month'] = pd.to_numeric(df_work['Month'], errors='coerce')
        invalid_mask |= (df_work['Month'] < 1) | (df_work['Month'] > 12) | (df_work['Month'].isnull())
        
    # 4. Invalid crime count detection (<0)
    if 'Crime_Count' in df_work.columns:
        df_work['Crime_Count'] = pd.to_numeric(df_work['Crime_Count'], errors='coerce')
        invalid_mask |= (df_work['Crime_Count'] < 0) | (df_work['Crime_Count'].isnull())
        
    # 5. Invalid population detection (<=0)
    if 'Population' in df_work.columns:
        df_work['Population'] = pd.to_numeric(df_work['Population'], errors='coerce')
        invalid_mask |= (df_work['Population'] <= 0) | (df_work['Population'].isnull())
        
    # 6. Invalid coordinates detection (Lat [-90, 90], Lon [-180, 180])
    if 'Latitude' in df_work.columns and 'Longitude' in df_work.columns:
        df_work['Latitude'] = pd.to_numeric(df_work['Latitude'], errors='coerce')
        df_work['Longitude'] = pd.to_numeric(df_work['Longitude'], errors='coerce')
        invalid_coord = (
            (df_work['Latitude'] < -90) | (df_work['Latitude'] > 90) |
            (df_work['Longitude'] < -180) | (df_work['Longitude'] > 180) |
            (df_work['Latitude'].isnull()) | (df_work['Longitude'].isnull())
        )
        invalid_mask |= invalid_coord
        
    invalid_records_count = int(invalid_mask.sum())
    
    # Filter out invalid records
    df_cleaned = df_work[~invalid_mask].copy()
    
    # 7. Data type conversion & standardization
    df_cleaned['Year'] = df_cleaned['Year'].astype(int)
    df_cleaned['Month'] = df_cleaned['Month'].astype(int)
    df_cleaned['Crime_Count'] = df_cleaned['Crime_Count'].astype(int)
    df_cleaned['Population'] = df_cleaned['Population'].astype(int)
    
    df_cleaned['City'] = df_cleaned['City'].astype(str).str.strip().str.title()
    df_cleaned['Area'] = df_cleaned['Area'].astype(str).str.strip().str.title()
    df_cleaned['Crime_Type'] = df_cleaned['Crime_Type'].astype(str).str.strip().str.title()
    df_cleaned['Severity'] = df_cleaned['Severity'].astype(str).str.strip().str.title()
    
    # Calculate Crime Rate on cleaned data
    df_cleaned = calculate_crime_rate(df_cleaned)
    
    stats = {
        'original_records': original_records,
        'clean_records': len(df_cleaned),
        'duplicates_removed': duplicates_count,
        'missing_values': missing_count,
        'invalid_records': invalid_records_count
    }
    
    return df_cleaned, stats
