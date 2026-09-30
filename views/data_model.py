import streamlit as st
import pandas as pd

def render_data_model_page():
    st.markdown("## 📐 Analytical Data Model Architecture")
    st.markdown("Structural definition of the analytical data schema, calculated metrics, and feature representations used in CRIME AI.")
    
    st.markdown("### 🧬 Analytical Flow Hierarchy")
    
    st.code("""
                  INDIAN CRIME DATASET
                           |
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
     LOCATION             TIME            CRIME TYPE
(Metropolitan Cities) (Year / Month)    (IPC / IT Act)
        |                  |                  |
        └──────────────────┼──────────────────┘
                           ↓
                      CRIME COUNT
                           ↓
                       POPULATION
                           ↓
                       CRIME RATE
                           ↓
               RANDOM FOREST REGRESSION
    """, language="text")
    
    st.markdown("---")
    st.markdown("### 📋 Field Dictionary & Data Attributes")
    
    field_data = [
        {"Field": "Year", "Type": "Integer", "Description": "Observation calendar year (2020-2025)", "Analytical Value": "Captures multi-year macro trends and long-term societal direction."},
        {"Field": "Month", "Type": "Integer / Categorical", "Description": "Observation month (1 - 12)", "Analytical Value": "Captures recurring seasonal spikes (e.g., festive season activity)."},
        {"Field": "City", "Type": "Categorical", "Description": "Major Indian municipality (Mumbai, Delhi, Bengaluru, etc.)", "Analytical Value": "Primary spatial dimension for metropolitan comparative modeling."},
        {"Field": "Area", "Type": "Categorical", "Description": "Sub-district, zone, or locality (e.g., Bandra, Dwarka)", "Analytical Value": "Granular location dimension for micro hotspot density identification."},
        {"Field": "Crime_Type", "Type": "Categorical", "Description": "Indian Offense Category (Theft, Cyber Crime, Robbery, etc.)", "Analytical Value": "Enables IPC category-specific predictive modeling."},
        {"Field": "Crime_Count", "Type": "Numerical (Integer)", "Description": "Raw total reported incident occurrences", "Analytical Value": "Fundamental numerator for rate computation."},
        {"Field": "Population", "Type": "Numerical (Integer)", "Description": "Total census population count of the area", "Analytical Value": "Standardization denominator removing urban density bias."},
        {"Field": "Severity", "Type": "Categorical", "Description": "Assigned offense gravity level (Low, Medium, High, Critical)", "Analytical Value": "Helps prioritize focus based on potential public impact."},
        {"Field": "Latitude", "Type": "Numerical (Float)", "Description": "WGS84 latitude coordinate in India", "Analytical Value": "Enables GIS mapping and spatial density clustering."},
        {"Field": "Longitude", "Type": "Numerical (Float)", "Description": "WGS84 longitude coordinate in India", "Analytical Value": "Enables GIS interactive map placement."},
        {"Field": "Crime_Rate", "Type": "Calculated Numerical", "Description": "Incidents per 100,000 residents", "Analytical Value": "Primary normalized target variable for ML regression modeling."}
    ]
    
    st.dataframe(pd.DataFrame(field_data))
    
    st.markdown("---")
    st.markdown("### 🧮 Mathematical Formulation")
    
    st.latex(r"\text{Crime Rate} = \left( \frac{\text{Crime Count}}{\text{Population}} \right) \times 100,000")
    
    st.markdown("""
    #### Example Calculation:
    * **Reported Crime Count:** 1,200 incidents
    * **District Population:** 8,500,000 residents
    "* **Calculated Crime Rate:** $(1,200 / 8,500,000) \\times 100,000 = \\mathbf{14.12}$ incidents per 100,000 people."
    
    *Standardizing per 100,000 population ensures fair comparisons between mega-cities like Mumbai/Delhi and smaller urban regions.*
    """)
