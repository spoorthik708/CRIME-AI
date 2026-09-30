import streamlit as st
import pandas as pd
from utils.visualization import render_folium_map

def render_crime_map_page():
    st.markdown("## 🗺️ Historical Indian Crime Hotspot Map (HeatMap Density)")
    st.markdown("Geospatial density visualization of reported crime incidents across major Indian metropolitan cities using Folium & OpenStreetMap.")
    
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

    # Spatial Filter Bar
    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1.4])
    cities = ['All Cities'] + sorted(list(df_cleaned['City'].unique()))
    selected_city = c1.selectbox("Filter Indian City", cities)
    
    types = ['All IPC Offenses'] + sorted(list(df_cleaned['Crime_Type'].unique()))
    selected_type = c2.selectbox("Filter Offense Category", types)
    
    severities = ['All Severities'] + sorted(list(df_cleaned['Severity'].unique()))
    selected_sev = c3.selectbox("Filter Severity Level", severities)
    
    map_mode = c4.selectbox(
        "Map Render Representation",
        ["Heatmap Density", "Heatmap + Pins", "Marker Pins"],
        index=0
    )
    
    map_df = df_cleaned.copy()
    if selected_city != 'All Cities':
        map_df = map_df[map_df['City'] == selected_city]
    if selected_type != 'All IPC Offenses':
        map_df = map_df[map_df['Crime_Type'] == selected_type]
    if selected_sev != 'All Severities':
        map_df = map_df[map_df['Severity'] == selected_sev]
        
    # Spatial Metrics Summary
    m1, m2, m3, m4 = st.columns(4)
    total_locations = len(map_df)
    avg_rate = map_df['Crime_Rate'].mean() if not map_df.empty else 0.0
    top_area = map_df.groupby('Area')['Crime_Count'].sum().idxmax() if not map_df.empty else "N/A"
    top_city = map_df.groupby('City')['Crime_Count'].sum().idxmax() if not map_df.empty else "N/A"
    
    m1.metric("Hotspot Locations", f"{total_locations:,}")
    m2.metric("Avg Regional Crime Rate", f"{avg_rate:.1f} / 100k")
    m3.metric("Highest Density City", top_city)
    m4.metric("Peak Incident Locality", top_area)
    
    st.markdown("---")
    st.markdown(f"### 📍 Interactive Geospatial Hotspots ({total_locations:,} Filtered Incident Points)")
    
    if map_df.empty:
        st.error("No coordinate observations found matching these filters.")
        return
        
    render_folium_map(map_df, height=600, map_mode=map_mode)
    
    st.info("💡 **Heatmap Reading Guide:** **Red Glow** indicates high-density incident clusters (hotspots), **Yellow/Green Glow** indicates moderate density, and **Cyan/Blue Glow** indicates lower density regions across Indian urban sectors.")

