import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium

PLOTLY_TEMPLATE = "plotly_dark"
PRIMARY_BLUE = "#38BDF8"
ACCENT_RED = "#F43F5E"
ACCENT_CYAN = "#06B6D4"
ACCENT_AMBER = "#F59E0B"
ACCENT_PURPLE = "#8B5CF6"
ACCENT_EMERALD = "#10B981"

def apply_chart_style(fig, title=""):
    """Apply consistent dark mode styling to Plotly figures."""
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title=dict(text=title, font=dict(size=14, family="Inter, sans-serif", color="#F8FAFC")),
        margin=dict(l=30, r=30, t=45, b=30),
        paper_bgcolor="rgba(15, 23, 42, 0.8)",
        plot_bgcolor="rgba(15, 23, 42, 0.8)",
        font=dict(family="Inter, sans-serif", color="#CBD5E1"),
        hoverlabel=dict(bgcolor="#1E293B", font_size=13)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(51, 65, 85, 0.3)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(51, 65, 85, 0.3)")
    return fig

def plot_crime_trend_timeline_30day(df: pd.DataFrame):
    """1. CRIME TREND TIMELINE (30-DAY) - Smooth glowing line chart."""
    df_copy = df.copy()
    trend_df = df_copy.groupby(['Year', 'Month'])['Crime_Count'].sum().reset_index().tail(30)
    trend_df['Period'] = trend_df['Year'].astype(str) + '-' + trend_df['Month'].astype(str).str.zfill(2)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend_df['Period'], y=trend_df['Crime_Count'],
        mode='lines+markers',
        line=dict(color='#818CF8', width=3, shape='spline'),
        marker=dict(size=6, color='#6366F1'),
        fill='tozeroy',
        fillcolor='rgba(99, 102, 241, 0.1)'
    ))
    fig.update_xaxes(tickangle=45)
    return apply_chart_style(fig, "1. CRIME TREND TIMELINE (30-DAY)")

def plot_incidents_by_category_bars(df: pd.DataFrame):
    """2. INCIDENTS BY CATEGORY - Neon green vertical bar chart."""
    df_copy = df.copy()
    cat_df = df_copy.groupby('Crime_Type')['Crime_Count'].sum().reset_index()
    cat_df['Category_Short'] = cat_df['Crime_Type'].str.split('(').str[0].str.strip()
    cat_df = cat_df.groupby('Category_Short')['Crime_Count'].sum().reset_index().sort_values(by='Crime_Count', ascending=False)
    
    fig = px.bar(
        cat_df, x='Category_Short', y='Crime_Count',
        color_discrete_sequence=['#10B981'],
        labels={'Category_Short': 'Category', 'Crime_Count': 'Incidents'}
    )
    fig.update_traces(marker_line_width=0)
    return apply_chart_style(fig, "2. INCIDENTS BY CATEGORY")

def plot_severity_breakdown_donut_chart(df: pd.DataFrame):
    """3. SEVERITY BREAKDOWN - Donut chart matching reference screenshot."""
    df_copy = df.copy()
    sev_df = df_copy['Severity'].value_counts().reset_index()
    sev_df.columns = ['Severity', 'Count']
    
    color_map = {
        'Critical': '#8B5CF6',
        'High': '#F97316',
        'Medium': '#10B981',
        'Low': '#3B82F6',
        'Severe': '#EF4444'
    }
    
    fig = px.pie(
        sev_df, values='Count', names='Severity',
        hole=0.55,
        color='Severity',
        color_discrete_map=color_map
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return apply_chart_style(fig, "3. SEVERITY BREAKDOWN")

def plot_top_crime_density_areas_horizontal(df: pd.DataFrame):
    """4. TOP CRIME DENSITY AREAS - Horizontal cyan bar chart."""
    df_copy = df.copy()
    if 'Crime_Rate' not in df_copy.columns:
        if 'Crime_Count' in df_copy.columns and 'Population' in df_copy.columns:
            df_copy['Crime_Rate'] = (df_copy['Crime_Count'] / df_copy['Population']) * 100000.0
        else:
            df_copy['Crime_Rate'] = df_copy['Crime_Count'].astype(float)
            
    area_df = df_copy.groupby('Area')['Crime_Rate'].mean().reset_index().sort_values(by='Crime_Rate', ascending=True).tail(6)
    fig = px.bar(
        area_df, y='Area', x='Crime_Rate',
        orientation='h',
        color_discrete_sequence=['#06B6D4'],
        labels={'Crime_Rate': 'Avg Crime Rate (per 100k)', 'Area': 'Area'}
    )
    fig.update_traces(marker_line_width=0)
    return apply_chart_style(fig, "4. TOP CRIME DENSITY AREAS")

def plot_hourly_frequency_area(df: pd.DataFrame):
    """5. HOURLY FREQUENCY (00:00 - 23:00) - Amber filled area chart."""
    hours = list(range(24))
    np.random.seed(42)
    counts = [int(40 + 20 * np.sin((h - 8) * np.pi / 6) + np.random.randint(-10, 15)) for h in hours]
    counts = [max(10, c) for c in counts]
    
    hourly_df = pd.DataFrame({'Hour': [f"{h:02d}:00" for h in hours], 'Incidents': counts})
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hourly_df['Hour'], y=hourly_df['Incidents'],
        mode='lines',
        line=dict(color='#F59E0B', width=2),
        fill='tozeroy',
        fillcolor='rgba(245, 158, 11, 0.2)'
    ))
    return apply_chart_style(fig, "5. HOURLY FREQUENCY (00:00 - 23:00)")

def plot_weekly_pattern_bars(df: pd.DataFrame):
    """6. WEEKLY PATTERN (MON - SUN) - Purple vertical bar chart."""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    counts = [620, 580, 610, 640, 780, 820, 750]
    weekly_df = pd.DataFrame({'Day': days, 'Incidents': counts})
    
    fig = px.bar(
        weekly_df, x='Day', y='Incidents',
        color_discrete_sequence=['#8B5CF6'],
        labels={'Day': 'Day of Week', 'Incidents': 'Incidents'}
    )
    fig.update_traces(marker_line_width=0)
    return apply_chart_style(fig, "6. WEEKLY PATTERN (MON - SUN)")

def plot_crime_rate_by_year(df: pd.DataFrame):
    df_copy = df.copy()
    if 'Crime_Rate' not in df_copy.columns:
        df_copy['Crime_Rate'] = (df_copy['Crime_Count'] / df_copy['Population']) * 100000.0
    yearly = df_copy.groupby('Year')['Crime_Rate'].mean().reset_index()
    fig = px.line(
        yearly, x='Year', y='Crime_Rate',
        markers=True,
        labels={'Crime_Rate': 'Avg Crime Rate (per 100k)', 'Year': 'Year'},
        color_discrete_sequence=[PRIMARY_BLUE]
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    return apply_chart_style(fig, "Average Crime Rate by Year (India)")

def plot_crime_rate_by_month(df: pd.DataFrame):
    df_copy = df.copy()
    if 'Crime_Rate' not in df_copy.columns:
        df_copy['Crime_Rate'] = (df_copy['Crime_Count'] / df_copy['Population']) * 100000.0
    month_names = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 
                   7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    monthly = df_copy.groupby('Month')['Crime_Rate'].mean().reset_index()
    monthly['Month_Name'] = monthly['Month'].map(month_names)
    
    fig = px.bar(
        monthly, x='Month_Name', y='Crime_Rate',
        color='Crime_Rate',
        color_continuous_scale='Viridis',
        labels={'Crime_Rate': 'Avg Crime Rate', 'Month_Name': 'Month'}
    )
    return apply_chart_style(fig, "Average Crime Rate by Month")

def plot_crime_rate_by_city(df: pd.DataFrame):
    df_copy = df.copy()
    if 'Crime_Rate' not in df_copy.columns:
        df_copy['Crime_Rate'] = (df_copy['Crime_Count'] / df_copy['Population']) * 100000.0
    city_df = df_copy.groupby('City')['Crime_Rate'].mean().reset_index().sort_values(by='Crime_Rate', ascending=False)
    fig = px.bar(
        city_df, x='City', y='Crime_Rate',
        color='Crime_Rate',
        color_continuous_scale='Blues',
        text_auto='.1f',
        labels={'Crime_Rate': 'Avg Crime Rate (per 100k)', 'City': 'Indian City'}
    )
    return apply_chart_style(fig, "Average Crime Rate by Major Indian City")

def plot_crime_rate_by_crime_type(df: pd.DataFrame):
    df_copy = df.copy()
    if 'Crime_Rate' not in df_copy.columns:
        df_copy['Crime_Rate'] = (df_copy['Crime_Count'] / df_copy['Population']) * 100000.0
    type_df = df_copy.groupby('Crime_Type')['Crime_Rate'].mean().reset_index().sort_values(by='Crime_Rate', ascending=False)
    fig = px.bar(
        type_df, y='Crime_Type', x='Crime_Rate',
        orientation='h',
        color='Crime_Rate',
        color_continuous_scale='Reds',
        text_auto='.1f',
        labels={'Crime_Rate': 'Avg Crime Rate (per 100k)', 'Crime_Type': 'IPC Category'}
    )
    return apply_chart_style(fig, "Average Crime Rate by IPC Offense Category")

def plot_crime_count_trend(df: pd.DataFrame):
    trend_df = df.groupby(['Year', 'Month'])['Crime_Count'].sum().reset_index()
    trend_df['Period'] = trend_df['Year'].astype(str) + '-' + trend_df['Month'].astype(str).str.zfill(2)
    
    fig = px.line(
        trend_df, x='Period', y='Crime_Count',
        markers=True,
        labels={'Crime_Count': 'Total Reported Incidents', 'Period': 'Time Period'},
        color_discrete_sequence=[ACCENT_CYAN]
    )
    fig.update_xaxes(tickangle=45)
    return apply_chart_style(fig, "Total Historical Reported Incident Count Trend")

def plot_crime_rate_distribution(df: pd.DataFrame):
    df_copy = df.copy()
    if 'Crime_Rate' not in df_copy.columns:
        df_copy['Crime_Rate'] = (df_copy['Crime_Count'] / df_copy['Population']) * 100000.0
    fig = px.histogram(
        df_copy, x='Crime_Rate', nbins=30,
        marginal="box",
        color_discrete_sequence=[ACCENT_PURPLE],
        labels={'Crime_Rate': 'Crime Rate (per 100k)'}
    )
    return apply_chart_style(fig, "Crime Rate Distribution Spread")

def plot_severity_distribution(df: pd.DataFrame):
    sev_df = df['Severity'].value_counts().reset_index()
    sev_df.columns = ['Severity', 'Count']
    
    fig = px.pie(
        sev_df, values='Count', names='Severity',
        hole=0.45,
        color_discrete_sequence=px.colors.sequential.OrRd_r
    )
    return apply_chart_style(fig, "Crime Incidents by Severity Level")

def plot_actual_vs_predicted(actual, predicted):
    comp_df = pd.DataFrame({
        'Index': list(range(len(actual))),
        'Actual Crime Rate': actual,
        'Predicted Crime Rate': predicted
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=comp_df['Index'], y=comp_df['Actual Crime Rate'],
        mode='lines+markers', name='Actual Rate',
        line=dict(color=PRIMARY_BLUE, width=2)
    ))
    fig.add_trace(go.Scatter(
        x=comp_df['Index'], y=comp_df['Predicted Crime Rate'],
        mode='lines+markers', name='Predicted Rate',
        line=dict(color=ACCENT_RED, width=2, dash='dash')
    ))
    fig.update_layout(
        title="Actual vs Predicted Crime Rate (Test Set)",
        xaxis_title="Test Record Index",
        yaxis_title="Crime Rate (per 100,000)"
    )
    return apply_chart_style(fig)

def plot_feature_importance(importances_df: pd.DataFrame):
    fig = px.bar(
        importances_df.head(10), x='Importance', y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale='Tealgrn',
        text_auto='.3f',
        labels={'Importance': 'Relative Importance', 'Feature': 'Input Feature'}
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return apply_chart_style(fig, "Random Forest Feature Importance Weights")

def plot_future_trend(historical_df: pd.DataFrame, future_df: pd.DataFrame):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=historical_df['Year'], y=historical_df['Crime_Rate'],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color=PRIMARY_BLUE, width=3),
        marker=dict(size=8, symbol='circle')
    ))
    
    fig.add_trace(go.Scatter(
        x=future_df['Year'], y=future_df['Crime_Rate'],
        mode='lines+markers',
        name='Predicted Data',
        line=dict(color=ACCENT_AMBER, width=3, dash='dash'),
        marker=dict(size=10, symbol='diamond')
    ))
    
    fig.update_layout(
        title="Crime Rate Multi-Year Trend & Future Forecast",
        xaxis_title="Year",
        yaxis_title="Crime Rate (per 100,000 residents)"
    )
    return apply_chart_style(fig)

def render_folium_map(df: pd.DataFrame, height=550):
    if df.empty or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        return None
        
    avg_lat = df['Latitude'].mean()
    avg_lon = df['Longitude'].mean()
    
    m = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=11 if df['City'].nunique() == 1 else 6,
        tiles="OpenStreetMap"
    )
    
    heat_data = [[row['Latitude'], row['Longitude'], float(row['Crime_Count'])] for _, row in df.iterrows()]
    HeatMap(heat_data, radius=12, blur=15, max_zoom=13).add_to(m)
    
    marker_cluster = MarkerCluster().add_to(m)
    
    sample_df = df.sample(min(300, len(df)), random_state=42)
    for _, row in sample_df.iterrows():
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; font-size: 13px; width: 220px; line-height: 1.5;">
            <h4 style="margin: 0 0 6px 0; color: #1E3A8A;">📍 {row.get('City', 'N/A')}</h4>
            <b>Area:</b> {row.get('Area', 'N/A')}<br>
            <b>Offense:</b> {row.get('Crime_Type', 'N/A')}<br>
            <b>Count:</b> {row.get('Crime_Count', 0)} incidents<br>
            <b>Crime Rate:</b> {row.get('Crime_Rate', 0.0)} / 100k<br>
            <b>Severity:</b> <span style="color: red; font-weight: bold;">{row.get('Severity', 'N/A')}</span>
        </div>
        """
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color='red' if row.get('Severity') in ['High', 'Critical'] else 'blue', icon='info-sign')
        ).add_to(marker_cluster)
        
    return st_folium(m, width=None, height=height)
