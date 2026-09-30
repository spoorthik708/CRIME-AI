import streamlit as st

def render_about_page():
    st.markdown("## ℹ️ About CRIME AI")
    st.markdown("### Crime Rate Prediction Using Historical Data (India)")
    
    st.markdown("---")
    st.markdown("### 📝 Problem Statement")
    st.info("""
    Historical crime data across Indian metropolitan areas (Mumbai, Delhi, Bengaluru, Kolkata, Chennai, etc.) contains valuable insights regarding offense categories, spatial distribution, time periods, and population density. Manually processing large historical crime datasets makes it challenging to uncover spatial trends or estimate future aggregate crime rates.

    **CRIME AI** automates this analytics workflow using Python predictive analytics, temporal lag feature engineering, Random Forest machine learning models, and interactive visualization dashboards.
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Core Academic Objectives")
    
    st.markdown("""
    1. **Data Ingestion:** Ingest custom CSV datasets or preloaded Indian metropolitan historical crime data.
    2. **Data Cleaning:** Automate data integrity audit checks for missing, duplicate, and out-of-bound entries.
    3. **Data Modeling:** Structure an analytical model separating spatial, temporal, and IPC offense category dimensions.
    4. **Crime Rate Calculation:** Standardize incident counts per 100,000 population.
    5. **Exploratory Analysis:** Analyze temporal, spatial, and severity distributions with Plotly charts.
    6. **Feature Engineering:** Calculate time-aware lag features (1M, 12M) and moving averages (3M, 6M, 12M).
    7. **Machine Learning:** Train Random Forest Regressor and Linear Regression models.
    8. **Crime Rate Prediction:** Predict future aggregate crime rates based on demographic and lag inputs.
    9. **Model Evaluation:** Measure performance using MAE, RMSE, R² scores, and feature importances.
    10. **Interactive Dashboard:** Present findings through an accessible Streamlit web application.
    """)
    
    st.markdown("---")
    st.markdown("### 🏗️ Project Architecture Diagram")
    
    st.code("""
             INDIAN HISTORICAL CRIME DATA
                          ↓
                   DATA INGESTION
                          ↓
                    DATA CLEANING
                          ↓
                    DATA MODELING
                          ↓
                 FEATURE ENGINEERING
                          ↓
                EXPLORATORY ANALYSIS
                          ↓
                 MACHINE LEARNING
                          ↓
                CRIME RATE PREDICTION
                          ↓
                 STREAMLIT DASHBOARD
                    ↙     ↓     ↘
                CHARTS   MAP  PREDICTION
    """, language="text")
    
    st.markdown("---")
    st.markdown("### 🔒 Data Privacy & Predictive Disclaimer")
    st.warning("""
    **CRIME AI** provides statistical estimates calculated from aggregate historical dataset patterns. Predictions represent macro trends and are not guaranteed individual outcomes. The system does NOT predict whether any specific individual will commit a crime, nor does it replace professional police analytics.
    """)
