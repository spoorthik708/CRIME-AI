import streamlit as st
import pandas as pd
from utils.visualization import (
    plot_crime_rate_by_year,
    plot_crime_rate_by_month,
    plot_crime_rate_by_city,
    plot_crime_rate_by_crime_type,
    plot_crime_count_trend,
    plot_crime_rate_distribution,
    plot_severity_distribution
)

def render_analysis_page():
    st.markdown("## 📊 Exploratory Crime Analysis (India)")
    st.markdown("Interactively analyze historical crime rates across spatial, temporal, and IPC category dimensions.")
    
    df_cleaned = st.session_state.get('df_cleaned', None)
    if df_cleaned is None:
        try:
            from utils.data_processing import clean_data
            raw = st.session_state.get('df_raw', pd.read_csv("data/sample_data.csv"))
            df_cleaned, _ = clean_data(raw)
            st.session_state['df_cleaned'] = df_cleaned
        except Exception:
            st.warning("Please load and clean dataset first.")
            return

    # Interactive Filters Bar
    st.markdown("### 🎛️ Dynamic Analytics Controls")
    f1, f2, f3, f4, f5 = st.columns(5)
    
    years = ['All'] + sorted(list(df_cleaned['Year'].unique()))
    selected_year = f1.selectbox("Filter Year", years)
    
    cities = ['All'] + sorted(list(df_cleaned['City'].unique()))
    selected_city = f2.selectbox("Filter Indian City", cities)
    
    areas = ['All']
    if selected_city != 'All':
        areas += sorted(list(df_cleaned[df_cleaned['City'] == selected_city]['Area'].unique()))
    else:
        areas += sorted(list(df_cleaned['Area'].unique()))
    selected_area = f3.selectbox("Filter Area / Zone", areas)
    
    types = ['All'] + sorted(list(df_cleaned['Crime_Type'].unique()))
    selected_type = f4.selectbox("IPC Crime Category", types)
    
    severities = ['All'] + sorted(list(df_cleaned['Severity'].unique()))
    selected_sev = f5.selectbox("Severity Level", severities)
    
    # Filter Execution
    filtered_df = df_cleaned.copy()
    if selected_year != 'All':
        filtered_df = filtered_df[filtered_df['Year'] == int(selected_year)]
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    if selected_area != 'All':
        filtered_df = filtered_df[filtered_df['Area'] == selected_area]
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['Crime_Type'] == selected_type]
    if selected_sev != 'All':
        filtered_df = filtered_df[filtered_df['Severity'] == selected_sev]
        
    st.info(f"Showing **{len(filtered_df):,}** observations matching selected analytical criteria.")
    
    if filtered_df.empty:
        st.error("No observations found for this filter combination. Please modify filter inputs.")
        return

    st.markdown("---")
    
    # Visualizations Layout
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_crime_rate_by_year(filtered_df))
    with c2:
        st.plotly_chart(plot_crime_rate_by_month(filtered_df))
        
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(plot_crime_rate_by_city(filtered_df))
    with c4:
        st.plotly_chart(plot_crime_rate_by_crime_type(filtered_df))
        
    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(plot_crime_count_trend(filtered_df))
    with c6:
        st.plotly_chart(plot_crime_rate_distribution(filtered_df))
        
    c7, c8 = st.columns(2)
    with c7:
        st.plotly_chart(plot_severity_distribution(filtered_df))
    with c8:
        st.markdown("### 🏆 Top High-Density Areas by Crime Rate")
        top_areas = filtered_df.groupby(['City', 'Area']).agg(
            Avg_Crime_Rate=('Crime_Rate', 'mean'),
            Total_Incidents=('Crime_Count', 'sum'),
            Avg_Population=('Population', 'mean')
        ).reset_index().sort_values(by='Avg_Crime_Rate', ascending=False).head(10)
        
        top_areas['Avg_Crime_Rate'] = top_areas['Avg_Crime_Rate'].round(2)
        top_areas['Avg_Population'] = top_areas['Avg_Population'].astype(int)
        st.dataframe(top_areas)
