import streamlit as st
import pandas as pd
import plotly.express as px
from utils.visualization import apply_chart_style

def render_crime_type_analysis_page():
    st.markdown("## 🏷️ IPC & IT Act Crime Category Analysis")
    st.markdown("Deep-dive analytics into auto-detected Indian penal code (IPC) and IT Act offense categories present in the dataset.")
    
    df_cleaned = st.session_state.get('df_cleaned', None)
    if df_cleaned is None:
        st.warning("Please load and clean dataset first.")
        return
        
    detected_types = sorted(list(df_cleaned['Crime_Type'].unique()))
    st.info(f"Auto-detected **{len(detected_types)}** IPC Offense Categories: {', '.join(detected_types)}")
    
    selected_type = st.selectbox("Select Offense Category for Analytical Breakdown", options=detected_types)
    
    type_df = df_cleaned[df_cleaned['Crime_Type'] == selected_type].copy()
    
    st.markdown("---")
    st.markdown(f"### 📊 Profile for **{selected_type}**")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Incidents", f"{type_df['Crime_Count'].sum():,}")
    c2.metric("Average Crime Rate", f"{type_df['Crime_Rate'].mean():.2f} / 100k")
    c3.metric("Peak Season Month", f"Month {type_df.groupby('Month')['Crime_Count'].sum().idxmax()}")
    c4.metric("Peak Area Crime Rate", f"{type_df.groupby('Area')['Crime_Rate'].mean().max():.2f} / 100k")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        yearly_type = type_df.groupby('Year').agg(
            Avg_Rate=('Crime_Rate', 'mean'),
            Total_Count=('Crime_Count', 'sum')
        ).reset_index()
        fig_yr = px.line(
            yearly_type, x='Year', y='Avg_Rate', markers=True,
            title=f"Yearly Trend for {selected_type}",
            labels={'Avg_Rate': 'Avg Crime Rate (per 100k)'}
        )
        st.plotly_chart(apply_chart_style(fig_yr))
        
    with col2:
        month_names = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 
                       7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        monthly_type = type_df.groupby('Month')['Crime_Rate'].mean().reset_index()
        monthly_type['Month_Name'] = monthly_type['Month'].map(month_names)
        fig_mo = px.bar(
            monthly_type, x='Month_Name', y='Crime_Rate',
            title=f"Monthly Seasonality for {selected_type}",
            labels={'Crime_Rate': 'Avg Crime Rate'}
        )
        st.plotly_chart(apply_chart_style(fig_mo))
        
    st.markdown("### 🗺️ Incident Share Across Major Indian Cities")
    city_type = type_df.groupby('City')['Crime_Count'].sum().reset_index()
    fig_city = px.pie(
        city_type, values='Crime_Count', names='City', hole=0.4,
        title=f"Distribution of {selected_type} across Indian Metropolitan Cities"
    )
    st.plotly_chart(apply_chart_style(fig_city))
