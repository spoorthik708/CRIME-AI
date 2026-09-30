import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

def render_live_simulation_page():
    st.markdown("## ⚡ Real-Time Crime Alert & Stream Simulation")
    st.markdown("Demonstration of real-time incident event ingestion, live alert processing, and dynamic metric updates across Indian Metropolitan Police Jurisdictions.")
    
    st.warning("⚠️ **SIMULATED REAL-TIME STREAM — NOT LIVE POLICE DISPATCH DATA.** This module simulates newly arriving event alerts for academic predictive streaming demonstration.")
    
    # Emergency Helpline Cards Bar
    st.markdown("### 🚨 Indian National Emergency Helplines")
    h1, h2, h3, h4 = st.columns(4)
    h1.markdown("""
    <div style="background-color: #1E293B; border-left: 4px solid #EF4444; padding: 12px; border-radius: 8px;">
        <span style="color: #94A3B8; font-size: 11px;">NATIONAL EMERGENCY</span><br>
        <b style="color: #EF4444; font-size: 20px;">📞 112</b>
    </div>
    """, unsafe_allow_html=True)
    h2.markdown("""
    <div style="background-color: #1E293B; border-left: 4px solid #38BDF8; padding: 12px; border-radius: 8px;">
        <span style="color: #94A3B8; font-size: 11px;">CYBER CRIME HELPLINE</span><br>
        <b style="color: #38BDF8; font-size: 20px;">💻 1930</b>
    </div>
    """, unsafe_allow_html=True)
    h3.markdown("""
    <div style="background-color: #1E293B; border-left: 4px solid #F59E0B; padding: 12px; border-radius: 8px;">
        <span style="color: #94A3B8; font-size: 11px;">WOMEN HELPLINE</span><br>
        <b style="color: #F59E0B; font-size: 20px;">🚺 1091</b>
    </div>
    """, unsafe_allow_html=True)
    h4.markdown("""
    <div style="background-color: #1E293B; border-left: 4px solid #10B981; padding: 12px; border-radius: 8px;">
        <span style="color: #94A3B8; font-size: 11px;">SENIOR CITIZEN LINE</span><br>
        <b style="color: #10B981; font-size: 20px;">👴 14567</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Initialize simulation state
    if 'sim_running' not in st.session_state:
        st.session_state['sim_running'] = False
    if 'sim_records' not in st.session_state:
        st.session_state['sim_records'] = []
        
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("▶️ START REAL-TIME STREAM", type="primary"):
            st.session_state['sim_running'] = True
    with c2:
        if st.button("⏹️ STOP REAL-TIME STREAM"):
            st.session_state['sim_running'] = False
    with c3:
        if st.button("🧹 Clear Alert Stream Buffer"):
            st.session_state['sim_records'] = []
            st.rerun()

    status_str = "🟢 LIVE STREAM ACTIVE" if st.session_state['sim_running'] else "🔴 STREAM PAUSED"
    st.markdown(f"**Stream Status:** `{status_str}` | Ingested Realtime Alerts: **{len(st.session_state['sim_records'])}**")
    
    st.markdown("---")
    
    feed_container = st.container()
    
    # Indian Police Jurisdiction Database
    police_stations = [
        ('Mumbai', 'Bandra Police Station', 'Bandra West', 19.0596, 72.8295),
        ('Mumbai', 'Colaba PS', 'Colaba', 18.9067, 72.8147),
        ('Delhi NCR', 'Connaught Place PS', 'Connaught Place', 28.6304, 77.2177),
        ('Delhi NCR', 'Dwarka Sector 23 PS', 'Dwarka', 28.5921, 77.0460),
        ('Bengaluru', 'Koramangala Police Station', 'Koramangala', 12.9352, 77.6245),
        ('Bengaluru', 'Indiranagar PS', 'Indiranagar', 12.9784, 77.6408),
        ('Kolkata', 'Park Street Police Station', 'Park Street', 22.5551, 88.3518),
        ('Chennai', 'T. Nagar PS', 'T. Nagar', 13.0418, 80.2341),
        ('Hyderabad', 'Banjara Hills PS', 'Banjara Hills', 17.4156, 78.4347),
        ('Pune', 'Hinjewadi Police Station', 'Hinjewadi IT Park', 18.5912, 73.7389)
    ]
    
    crime_types = [
        ('Theft (IPC 379)', 'Low'),
        ('Cyber Crime (IT Act)', 'Medium'),
        ('Vehicle Theft (IPC 379)', 'Medium'),
        ('Burglary / Housebreak (IPC 457)', 'Medium'),
        ('Financial Fraud (IPC 420)', 'Medium'),
        ('Robbery & Snatching (IPC 392)', 'High'),
        ('Assault & Hurt (IPC 354/323)', 'Critical')
    ]
    
    if st.session_state['sim_running']:
        ps_info = police_stations[np.random.choice(len(police_stations))]
        crime_info = crime_types[np.random.choice(len(crime_types))]
        now = datetime.now()
        
        new_event = {
            'Time': now.strftime("%H:%M:%S"),
            'Date': now.strftime("%Y-%m-%d"),
            'City': ps_info[0],
            'Police_Station': ps_info[1],
            'Area': ps_info[2],
            'Crime_Type': crime_info[0],
            'Severity': crime_info[1],
            'Crime_Count': int(np.random.randint(1, 4)),
            'Population': 850000,
            'Latitude': ps_info[3] + np.random.uniform(-0.005, 0.005),
            'Longitude': ps_info[4] + np.random.uniform(-0.005, 0.005)
        }
        
        st.session_state['sim_records'].append(new_event)
        
    with feed_container:
        if st.session_state['sim_records']:
            latest = st.session_state['sim_records'][-1]
            sev_color = "#EF4444" if latest['Severity'] in ['High', 'Critical'] else "#38BDF8"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border: 2px solid {sev_color}; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.4);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin:0; color:{sev_color}; font-size: 16px;">⚡ REALTIME ALERT INGESTED</h4>
                    <span style="background-color: {sev_color}; color: #FFFFFF; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px;">{latest['Severity'].upper()} SEVERITY</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 15px; margin-top: 14px; color: #E2E8F0; font-family: monospace; font-size: 13px;">
                    <div><b>Timestamp:</b> {latest['Time']}</div>
                    <div><b>City:</b> {latest['City']}</div>
                    <div><b>Jurisdiction:</b> {latest['Police_Station']}</div>
                    <div><b>Area:</b> {latest['Area']}</div>
                    <div><b>Offense:</b> {latest['Crime_Type']}</div>
                    <div><b>Incidents:</b> {latest['Crime_Count']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            sim_df = pd.DataFrame(st.session_state['sim_records'])
            sim_df['Crime_Rate'] = (sim_df['Crime_Count'] / sim_df['Population']) * 100000.0
            
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Ingested Alert Buffer", f"{len(sim_df)}")
            sc2.metric("Total Incident Count", f"{sim_df['Crime_Count'].sum()}")
            sc3.metric("Stream Average Rate", f"{sim_df['Crime_Rate'].mean():.2f} / 100k")
            
            st.markdown("#### Real-time Ingestion Alert Log")
            st.dataframe(sim_df[['Time', 'City', 'Police_Station', 'Area', 'Crime_Type', 'Severity', 'Crime_Count']].tail(10))
        else:
            st.info("Click '▶️ START REAL-TIME STREAM' to launch dynamic incident alerting across Indian metropolitan police jurisdictions.")
            
    if st.session_state['sim_running']:
        time.sleep(2)
        st.rerun()
