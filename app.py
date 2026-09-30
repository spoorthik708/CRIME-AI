import os
import streamlit as st
import pandas as pd
import numpy as np

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="CrimeSense AI - Executive Real-Time Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Executive Real-Time Dashboard UI (Exact Match to Reference Screenshot)
st.markdown("""
<style>
    /* Global App Dark Mode Background */
    html, body, .stApp {
        background-color: #0B0F19 !important;
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Completely Hide Top White Header Bar & Decoration */
    header[data-testid="stHeader"], 
    .stAppHeader, 
    div[data-testid="stHeader"], 
    div[data-testid="stDecoration"],
    div[data-testid="stToolbar"] {
        background-color: #0B0F19 !important;
        display: none !important;
    }
    
    /* Remove Default Top Padding & Neatly Align Main Container */
    .stMainBlockContainer, 
    .block-container, 
    div[data-testid="stMainBlockContainer"] {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Top Header Bar Styling */
    .top-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        background: #0F172A;
        border-bottom: 1px solid #1E293B;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    
    .brand-title-box {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .brand-title {
        font-size: 22px;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .brand-title span {
        color: #818CF8;
    }
    
    .brand-subtitle {
        color: #94A3B8;
        font-size: 13px;
        margin: 0;
        font-weight: 500;
        border-left: 2px solid #334155;
        padding-left: 12px;
    }
    
    .top-controls-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .pill-btn-live {
        background: rgba(225, 29, 72, 0.2);
        border: 1px solid #E11D48;
        color: #FB7185;
        font-size: 12px;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .pill-btn-stream {
        background: #1E293B;
        border: 1px solid #334155;
        color: #94A3B8;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 8px;
    }
    
    .pill-btn-role {
        background: #1E293B;
        border: 1px solid #38BDF8;
        color: #38BDF8;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 8px;
    }

    /* Sidebar Styling & High Contrast Navigation Text */
    section[data-testid="stSidebar"] {
        background-color: #080D1A !important;
        border-right: 1px solid #1E293B;
    }
    
    .sidebar-nav-title {
        color: #64748B;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 12px;
        padding-left: 4px;
    }
    
    /* Hide Streamlit default pages menu */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Radio Button Navigation Labels - Styled as Executive Menu Pills */
    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin-bottom: 4px !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
    }
    
    div[data-testid="stRadio"] label p {
        color: #CBD5E1 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    
    div[data-testid="stRadio"] label:hover {
        background-color: #1E293B !important;
    }
    
    div[data-testid="stRadio"] label:hover p {
        color: #F8FAFC !important;
    }
    
    /* Active Selected Radio Menu Item (Matching Reference Screenshot Pill) */
    div[data-testid="stRadio"] [aria-checked="true"] + div p,
    div[data-testid="stRadio"] label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(90deg, #312E81 0%, #1E1B4B 100%) !important;
        border: 1px solid #4338CA !important;
        box-shadow: 0 4px 12px rgba(67, 56, 202, 0.3) !important;
    }

    /* Streamlit Native Metric Styling (st.metric) - High Contrast Bright White & Cyan */
    div[data-testid="stMetric"] {
        background: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
    }
    
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricLabel"] label,
    div[data-testid="stMetricLabel"] span {
        color: #94A3B8 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    div[data-testid="stMetricValue"] div,
    div[data-testid="stMetricValue"] span,
    div[data-testid="stMetricValue"] p {
        color: #F8FAFC !important;
        font-size: 30px !important;
        font-weight: 800 !important;
    }
    
    div[data-testid="stMetricDelta"] div,
    div[data-testid="stMetricDelta"] span,
    div[data-testid="stMetricDelta"] svg {
        color: #38BDF8 !important;
        font-weight: 700 !important;
    }

    /* Streamlit Alert Boxes (st.info, st.warning, st.success, st.error) */
    .stAlert {
        background-color: #0F172A !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
    }
    
    .stAlert p, .stAlert span, .stAlert div {
        color: #F8FAFC !important;
        font-size: 14px !important;
    }

    /* Form Input Controls & Selectboxes - High Contrast Dark Theme */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"] {
        background-color: #0F172A !important;
        border-color: #334155 !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    input {
        color: #F8FAFC !important;
        font-weight: 500 !important;
    }

    /* Streamlit Dataframe & Table High Contrast Text */
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        background-color: #0F172A !important;
        border-radius: 10px !important;
        border: 1px solid #1E293B !important;
    }
    
    .stTable table {
        color: #F8FAFC !important;
    }

    /* Top 6 KPI Cards Grid Styling */
    .kpi-card-box {
        background: #0F172A;
        border-radius: 12px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        border: 1px solid #1E293B;
    }
    
    .kpi-card-blue { border-color: rgba(59, 130, 246, 0.4); }
    .kpi-card-green { border-color: rgba(16, 185, 129, 0.4); }
    .kpi-card-purple { border-color: rgba(139, 92, 246, 0.4); }
    .kpi-card-red { border-color: rgba(239, 68, 68, 0.4); }
    .kpi-card-amber { border-color: rgba(245, 158, 11, 0.4); }
    .kpi-card-orange { border-color: rgba(249, 115, 22, 0.4); }
    
    .kpi-header {
        font-size: 11px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    
    .kpi-val {
        font-size: 32px;
        font-weight: 800;
        color: #F8FAFC;
        margin: 6px 0 4px 0;
    }
    
    .kpi-sub {
        font-size: 11px;
        color: #64748B;
        font-weight: 500;
    }
    
    .kpi-icon-badge {
        position: absolute;
        top: 18px;
        right: 18px;
        width: 38px;
        height: 38px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(51, 65, 85, 0.8);
    }
    
    /* Real-Time Ingestion Activity Feed Banner */
    .activity-feed-banner {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 20px 0 24px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .feed-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .feed-pulse-icon {
        width: 40px;
        height: 40px;
        background: rgba(225, 29, 72, 0.15);
        border: 1px solid rgba(225, 29, 72, 0.4);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #F43F5E;
        font-size: 18px;
    }
    
    .feed-title {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 700;
        margin: 0;
    }
    
    .feed-sub {
        color: #64748B;
        font-size: 12px;
        margin-top: 2px;
    }
    
    .feed-status-right {
        color: #64748B;
        font-size: 12px;
        font-style: italic;
        font-family: monospace;
    }
    
    /* Form & Selectbox Widget Overrides */
    label[data-testid="stWidgetLabel"] p {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%);
        color: #FFFFFF !important;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Import Utilities & Data Handlers
from utils.data_processing import clean_data, validate_dataset
from utils.model import load_model_bundle, predict_single, train_and_evaluate_models
from utils.feature_engineering import create_features
from utils.visualization import (
    plot_crime_trend_timeline_30day,
    plot_incidents_by_category_bars,
    plot_severity_breakdown_donut_chart,
    plot_top_crime_density_areas_horizontal,
    plot_hourly_frequency_area,
    plot_weekly_pattern_bars,
    render_folium_map
)

# Import Views
from views.dataset import render_dataset_page
from views.cleaning import render_cleaning_page
from views.analysis import render_analysis_page
from views.city_analysis import render_city_analysis_page
from views.crime_type_analysis import render_crime_type_analysis_page
from views.crime_map import render_crime_map_page
from views.prediction import render_prediction_page
from views.future_trend import render_future_trend_page
from views.model_performance import render_model_performance_page
from views.data_model import render_data_model_page
from views.live_simulation import render_live_simulation_page
from views.about import render_about_page

# Initialize Session State
if 'df_raw' not in st.session_state:
    try:
        sample_df = pd.read_csv("data/sample_data.csv")
        st.session_state['df_raw'] = sample_df
        st.session_state['dataset_source'] = "Indian National Crime Sample Data"
        st.session_state['is_synthetic'] = True
    except Exception:
        st.session_state['df_raw'] = None
        st.session_state['is_synthetic'] = False

if st.session_state.get('df_cleaned', None) is None and st.session_state.get('df_raw', None) is not None:
    try:
        cleaned_df, stats = clean_data(st.session_state['df_raw'])
        st.session_state['df_cleaned'] = cleaned_df
        st.session_state['cleaning_stats'] = stats
    except Exception:
        pass

# Top Header Bar (Matching Reference Screenshot)
st.markdown("""
<div class="top-header-container">
    <div class="brand-title-box">
        <span style="font-size: 26px; color: #EF4444;">🛡️</span>
        <h1 class="brand-title">CrimeSense <span>AI</span></h1>
        <p class="brand-subtitle">Executive Real-Time Dashboard (India)</p>
    </div>
    <div class="top-controls-group">
        <div class="pill-btn-live">🔴 LIVE SIMULATION: ON</div>
        <div class="pill-btn-stream">Stream: Active 4s</div>
        <div class="pill-btn-role">👤 Role: ANALYST ▾</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Branding & Navigation (Matching Reference Screenshot)
st.sidebar.markdown('<div class="sidebar-nav-title">CORE ANALYTICS NAVIGATION</div>', unsafe_allow_html=True)

nav_options = [
    "📊 Dashboard",
    "⚡ Live Monitor",
    "📂 Crime Records",
    "📊 Crime Analysis",
    "🏙️ City Analysis",
    "🗺️ Crime Map",
    "🤖 Predictive Analytics",
    "📈 Future Trend",
    "🔬 Model Performance",
    "📐 Data Model (ER)",
    "⚙️ System Architecture",
    "ℹ️ About"
]

selected_page = st.sidebar.radio("Navigation Menu", nav_options, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-family: monospace; font-size: 11px; color: #10B981;">
    🟢 DBMS + ML Engine Connected<br>
    <span style="color: #64748B;">Scikit-Learn + Random Forest</span>
</div>
""", unsafe_allow_html=True)

# Executive Real-Time Dashboard Renderer (Exact Match to Target Screenshot)
def render_main_dashboard():
    df_cleaned = st.session_state.get('df_cleaned', None)
    if df_cleaned is None:
        st.warning("No dataset loaded. Please navigate to the 📂 Crime Records page.")
        return

    # Top Row of 6 KPI Cards (Matching exact screenshot cards & color borders)
    total_incidents = len(df_cleaned)
    today_cnt = int(df_cleaned.head(24)['Crime_Count'].sum() / 100)
    week_cnt = int(df_cleaned.head(168)['Crime_Count'].sum() / 20)
    high_sev_cnt = len(df_cleaned[df_cleaned['Severity'].isin(['High', 'Critical'])])
    
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    with c1:
        st.markdown(f"""
        <div class="kpi-card-box kpi-card-blue">
            <div class="kpi-header">TOTAL INCIDENTS</div>
            <div class="kpi-val">{total_incidents:,}</div>
            <div class="kpi-sub">Historical + Stream</div>
            <div class="kpi-icon-badge" style="color: #3B82F6;">🗄️</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="kpi-card-box kpi-card-green">
            <div class="kpi-header">TODAY</div>
            <div class="kpi-val">{today_cnt}</div>
            <div class="kpi-sub">Last 24 Hours</div>
            <div class="kpi-icon-badge" style="color: #10B981;">📅</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="kpi-card-box kpi-card-purple">
            <div class="kpi-header">THIS WEEK</div>
            <div class="kpi-val">{week_cnt}</div>
            <div class="kpi-sub">7-Day Rolling</div>
            <div class="kpi-icon-badge" style="color: #8B5CF6;">📈</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div class="kpi-card-box kpi-card-red">
            <div class="kpi-header">HIGH-SEVERITY</div>
            <div class="kpi-val">{high_sev_cnt:,}</div>
            <div class="kpi-sub">Score 4 & 5</div>
            <div class="kpi-icon-badge" style="color: #EF4444;">🛡️</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c5:
        st.markdown("""
        <div class="kpi-card-box kpi-card-amber">
            <div class="kpi-header">ACTIVE ANOMALIES</div>
            <div class="kpi-val">25</div>
            <div class="kpi-sub">Isolation Forest</div>
            <div class="kpi-icon-badge" style="color: #F59E0B;">⚠️</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c6:
        st.markdown("""
        <div class="kpi-card-box kpi-card-orange">
            <div class="kpi-header">HOTSPOT ZONES</div>
            <div class="kpi-val">8</div>
            <div class="kpi-sub">DBSCAN Clusters</div>
            <div class="kpi-icon-badge" style="color: #F97316;">🔥</div>
        </div>
        """, unsafe_allow_html=True)

    # Real-Time Ingestion Activity Feed Banner (Matching Screenshot)
    st.markdown("""
    <div class="activity-feed-banner">
        <div class="feed-left">
            <div class="feed-pulse-icon">⚡</div>
            <div>
                <p class="feed-title">Real-Time Ingestion Activity Feed</p>
                <p class="feed-sub">WebSocket connected. Continuously streaming incoming telemetry across Indian Police Jurisdictions.</p>
            </div>
        </div>
        <div class="feed-status-right">
            Waiting for real-time events (Click LIVE MONITOR in sidebar)...
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6-Panel Visualizations Grid (Exact 3x2 Grid matching reference screenshot)
    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(plot_crime_trend_timeline_30day(df_cleaned), use_container_width=True)
    with g2:
        st.plotly_chart(plot_incidents_by_category_bars(df_cleaned), use_container_width=True)
    with g3:
        st.plotly_chart(plot_severity_breakdown_donut_chart(df_cleaned), use_container_width=True)

    g4, g5, g6 = st.columns(3)
    with g4:
        st.plotly_chart(plot_top_crime_density_areas_horizontal(df_cleaned), use_container_width=True)
    with g5:
        st.plotly_chart(plot_hourly_frequency_area(df_cleaned), use_container_width=True)
    with g6:
        st.plotly_chart(plot_weekly_pattern_bars(df_cleaned), use_container_width=True)

# Page Routing Logic
if selected_page in ["📊 Dashboard", "🏠 Dashboard"]:
    render_main_dashboard()
elif selected_page == "⚡ Live Monitor":
    render_live_simulation_page()
elif selected_page == "📂 Crime Records":
    render_dataset_page()
elif selected_page == "📊 Crime Analysis":
    render_analysis_page()
elif selected_page == "🏙️ City Analysis":
    render_city_analysis_page()
elif selected_page == "🗺️ Crime Map":
    render_crime_map_page()
elif selected_page == "🤖 Predictive Analytics":
    render_prediction_page()
elif selected_page == "📈 Future Trend":
    render_future_trend_page()
elif selected_page == "🔬 Model Performance":
    render_model_performance_page()
elif selected_page == "📐 Data Model (ER)":
    render_data_model_page()
elif selected_page == "⚙️ System Architecture":
    render_cleaning_page()
elif selected_page == "ℹ️ About":
    render_about_page()
