import streamlit as st
import pandas as pd
from utils.data_processing import clean_data

def render_cleaning_page():
    st.markdown("## 🧹 Automated Data Cleaning & Integrity Audit")
    st.markdown("Executes automated audit checks on raw crime data to detect missing values, duplicates, and out-of-bound entries before predictive modeling.")
    
    df_raw = st.session_state.get('df_raw', None)
    if df_raw is None:
        st.warning("No dataset loaded. Please navigate to the 📂 Dataset page first.")
        return
        
    cleaned_df, stats = clean_data(df_raw)
    st.session_state['df_cleaned'] = cleaned_df
    st.session_state['cleaning_stats'] = stats
    
    st.markdown("### 📈 Automated Data Audit Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Original Records", f"{stats['original_records']:,}")
    col2.metric("Clean Records", f"{stats['clean_records']:,}")
    col3.metric("Duplicates Removed", f"{stats['duplicates_removed']:,}")
    col4.metric("Missing Values", f"{stats['missing_values']:,}")
    col5.metric("Invalid Records", f"{stats['invalid_records']:,}")
    
    st.markdown("---")
    st.markdown("### ⚙️ Executed Cleaning Procedures")
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        #### 1. Audit & Integrity Operations
        * **Duplicate Removal:** Identified and dropped duplicate row observations.
        * **Missing Value Imputation/Filtering:** Handled null entries in critical columns.
        * **Invalid Year Detection:** Enforced valid observation range [1900, 2100].
        * **Negative Incident Count Checks:** Removed non-sensical negative counts.
        """)
        
    with p2:
        st.markdown("""
        #### 2. Geographic & Rate Standardization
        * **Population Audit:** Filtered out zero or negative census population numbers.
        * **Indian Coordinate Bounds:** Validated latitude [-90, 90] and longitude [-180, 180] bounds.
        * **Categorical Standardization:** Trimmed whitespace and converted Indian cities, areas, and IPC crime sections to Title Case.
        * **Crime Rate Formula:** Applied `Crime Rate = (Crime Count / Population) × 100,000`.
        """)
        
    st.markdown("---")
    st.markdown("### 📋 Cleaned Dataset Inspection")
    st.dataframe(cleaned_df.head(15))
    
    with st.expander("🔍 Cleaned Dataset Summary Statistics"):
        st.dataframe(cleaned_df.describe())
