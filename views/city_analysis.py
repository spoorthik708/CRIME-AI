import streamlit as st
import pandas as pd
import plotly.express as px
from utils.visualization import apply_chart_style

def render_city_analysis_page():
    st.markdown("## 🏙️ Indian City-Level Comparative Analytics")
    st.markdown("Perform objective comparative analysis across major Indian metropolitan centers (Mumbai, Delhi NCR, Bengaluru, Kolkata, Chennai, Hyderabad, Pune, Ahmedabad).")
    
    df_cleaned = st.session_state.get('df_cleaned', None)
    if df_cleaned is None:
        st.warning("Please load and clean the dataset first.")
        return
        
    all_cities = sorted(list(df_cleaned['City'].unique()))
    selected_cities = st.multiselect("Select Indian Cities to Compare", options=all_cities, default=all_cities[:4])
    
    if not selected_cities:
        st.info("Select at least one city to render comparative stats.")
        return
        
    city_df = df_cleaned[df_cleaned['City'].isin(selected_cities)].copy()
    
    st.markdown("---")
    st.markdown("### 📊 City Aggregate Statistics")
    
    summary_table = city_df.groupby('City').agg(
        Average_Crime_Rate=('Crime_Rate', 'mean'),
        Total_Incidents=('Crime_Count', 'sum'),
        Average_Population=('Population', 'mean'),
        Observed_Years=('Year', lambda x: f"{x.min()} - {x.max()}")
    ).reset_index()
    
    summary_table['Average_Crime_Rate'] = summary_table['Average_Crime_Rate'].round(2)
    summary_table['Average_Population'] = summary_table['Average_Population'].astype(int)
    
    st.dataframe(summary_table)
    
    st.markdown("---")
    st.markdown("### 📈 Historical Rate Comparison Across Selected Cities")
    
    city_yearly = city_df.groupby(['Year', 'City'])['Crime_Rate'].mean().reset_index()
    fig_city = px.line(
        city_yearly, x='Year', y='Crime_Rate', color='City',
        markers=True,
        labels={'Crime_Rate': 'Avg Crime Rate (per 100k)', 'Year': 'Year'}
    )
    st.plotly_chart(apply_chart_style(fig_city, "Annual Crime Rate Trend by City"))
    
    c1, c2 = st.columns(2)
    with c1:
        type_by_city = city_df.groupby(['City', 'Crime_Type'])['Crime_Count'].sum().reset_index()
        fig_type = px.bar(
            type_by_city, x='City', y='Crime_Count', color='Crime_Type',
            barmode='stack',
            labels={'Crime_Count': 'Total Incident Count'}
        )
        st.plotly_chart(apply_chart_style(fig_type, "Crime Breakdown by IPC Category Across Selected Cities"))
        
    with c2:
        area_agg = city_df.groupby(['City', 'Area'])['Crime_Rate'].mean().reset_index().sort_values(by='Crime_Rate', ascending=False)
        fig_area = px.bar(
            area_agg, x='Area', y='Crime_Rate', color='City',
            labels={'Crime_Rate': 'Avg Crime Rate (per 100k)'}
        )
        st.plotly_chart(apply_chart_style(fig_area, "Sub-District / Area Crime Rate Distribution"))
        
    st.info("ℹ️ **Statistical Disclaimer:** All metrics reflect objective numerical aggregates calculated from the historical dataset and avoid subjective qualitative judgments.")
