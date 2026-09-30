import streamlit as st
import pandas as pd
from utils.data_processing import validate_dataset, standardize_columns, REQUIRED_COLUMNS

def render_dataset_page():
    st.markdown("## 📂 Dataset Management & Ingestion")
    st.markdown("Upload historical Indian crime data CSV files or inspect the preloaded National Crime Analytics dataset.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload Historical Crime Dataset (CSV)", type=['csv'])
        if uploaded_file is not None:
            try:
                raw_df = pd.read_csv(uploaded_file)
                st.session_state['df_raw'] = raw_df
                st.session_state['dataset_source'] = "Uploaded Custom Dataset"
                st.session_state['is_synthetic'] = False
                st.success("✅ Successfully loaded custom CSV crime dataset!")
            except Exception as e:
                st.error(f"Error reading uploaded CSV file: {e}")
                
    with col2:
        st.markdown("### Preloaded Indian Dataset")
        if st.button("🔄 Reset / Load Indian Sample Data", type="primary"):
            try:
                sample_df = pd.read_csv("data/sample_data.csv")
                st.session_state['df_raw'] = sample_df
                st.session_state['dataset_source'] = "Indian National Crime Sample Data"
                st.session_state['is_synthetic'] = True
                st.success("Loaded default Indian metropolitan crime dataset!")
            except Exception as e:
                st.error(f"Could not load sample dataset: {e}")
                
    # Synthetic data disclaimer badge
    if st.session_state.get('is_synthetic', True):
        st.warning("⚠️ **DEMO / SYNTHETIC DATA** — Currently using synthetic Indian crime data for academic demonstration. Never present synthetic data as real official police crime records.")
    else:
        st.info(f"ℹ️ Active Dataset Source: **{st.session_state.get('dataset_source', 'Custom Data')}**")
        
    df_current = st.session_state.get('df_raw', None)
    
    if df_current is None:
        st.warning("No dataset loaded. Please upload a CSV file or reset to sample dataset.")
        return
        
    st.markdown("---")
    st.markdown("### 🔍 Dataset Validation")
    
    is_valid, missing_cols, df_std = validate_dataset(df_current)
    st.session_state['df_standardized'] = df_std
    
    if is_valid:
        st.success("✅ Dataset Validation Passed! All required schema fields are present.")
    else:
        st.error(f"❌ Dataset Validation Failed! Missing required columns: {', '.join(missing_cols)}")
        st.info("Expected schema fields: " + ", ".join(REQUIRED_COLUMNS))
        
    # Validation checklist grid
    with st.expander("📋 Required Schema Validation Checklist", expanded=False):
        check_cols = st.columns(5)
        for idx, col_name in enumerate(REQUIRED_COLUMNS):
            col_target = check_cols[idx % 5]
            if col_name in df_std.columns:
                col_target.markdown(f"✅ **{col_name}**")
            else:
                col_target.markdown(f"❌ **{col_name}**")
                
    st.markdown("---")
    st.markdown("### 📊 Dataset Overview")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Records", f"{len(df_std):,}")
    m2.metric("Total Schema Fields", f"{len(df_std.columns)}")
    m3.metric("Memory Footprint", f"{df_std.memory_usage().sum() / 1024:.1f} KB")
    m4.metric("Null Cell Count", f"{df_std.isnull().sum().sum()}")
    
    st.markdown("#### Sample Records Preview (Indian Cities)")
    st.dataframe(df_std.head(10))
    
    with st.expander("📈 Comprehensive Field Summary & Range Statistics"):
        st.dataframe(df_std.describe(include='all').fillna(''))
