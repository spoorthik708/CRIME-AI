import streamlit as st
import pandas as pd
from utils.model import load_model_bundle, predict_single, train_and_evaluate_models
from utils.feature_engineering import create_features

def render_prediction_page():
    st.markdown("## 🤖 Predict Future Crime Rate (India)")
    st.markdown("Specify prospective Indian urban location, demographic, and historical lag parameters to forecast aggregate crime rates using the trained Random Forest model.")
    
    df_cleaned = st.session_state.get('df_cleaned', None)
    
    bundle = load_model_bundle()
    if bundle is None:
        if df_cleaned is not None:
            with st.spinner("Auto-training machine learning model on dataset..."):
                try:
                    df_feat = create_features(df_cleaned)
                    train_and_evaluate_models(df_feat)
                    bundle = load_model_bundle()
                except Exception as e:
                    st.error(f"Could not train initial model: {e}")
                    return
        else:
            try:
                from utils.data_processing import clean_data
                raw = pd.read_csv("data/sample_data.csv")
                df_cleaned, _ = clean_data(raw)
                st.session_state['df_cleaned'] = df_cleaned
                df_feat = create_features(df_cleaned)
                train_and_evaluate_models(df_feat)
                bundle = load_model_bundle()
            except Exception as e:
                st.error("Please load dataset and train model first.")
                return

    cities = sorted(list(df_cleaned['City'].unique())) if df_cleaned is not None else ['Mumbai', 'Delhi NCR', 'Bengaluru']
    areas = sorted(list(df_cleaned['Area'].unique())) if df_cleaned is not None else ['Bandra West', 'Connaught Place', 'Indiranagar']
    crime_types = sorted(list(df_cleaned['Crime_Type'].unique())) if df_cleaned is not None else ['Theft (IPC 379)', 'Cyber Crime (IT Act)', 'Burglary / Housebreak (IPC 457)']
    severities = sorted(list(df_cleaned['Severity'].unique())) if df_cleaned is not None else ['Low', 'Medium', 'High', 'Critical']
    
    st.markdown("### 🎛️ Input Prediction Parameters")
    
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            city_in = st.selectbox("Target Indian City", cities)
            area_in = st.selectbox("Sub-District / Area", areas)
            crime_type_in = st.selectbox("IPC / Offense Category", crime_types)
            severity_in = st.selectbox("Severity Level", severities)
            
        with col2:
            year_in = st.number_input("Target Year", min_value=2020, max_value=2030, value=2026)
            month_in = st.slider("Target Month", min_value=1, max_value=12, value=6)
            pop_in = st.number_input("Estimated Area Population", min_value=10000, max_value=20000000, value=850000, step=25000)
            count_in = st.number_input("Estimated Reported Count", min_value=0, max_value=20000, value=150)
            
        with col3:
            prev_rate_in = st.number_input("Previous Crime Rate (per 100k)", min_value=0.0, max_value=5000.0, value=18.5)
            prev_yr_rate_in = st.number_input("Previous Year Crime Rate (per 100k)", min_value=0.0, max_value=5000.0, value=17.8)
            prev_mo_rate_in = st.number_input("Previous Month Crime Rate (per 100k)", min_value=0.0, max_value=5000.0, value=18.2)
            rolling_3m = st.number_input("Rolling 3-Month Average Rate", min_value=0.0, max_value=5000.0, value=18.0)
            
        submit_btn = st.form_submit_button("🔮 Predict Crime Rate", type="primary")
        
    if submit_btn or st.session_state.get('last_prediction', None) is not None:
        if submit_btn:
            input_dict = {
                'City': city_in,
                'Area': area_in,
                'Crime_Type': crime_type_in,
                'Severity': severity_in,
                'Year': year_in,
                'Month': month_in,
                'Population': pop_in,
                'Crime_Count': count_in,
                'Previous_Crime_Rate': prev_rate_in,
                'Previous_Year_Crime_Rate': prev_yr_rate_in,
                'Previous_Month_Crime_Rate': prev_mo_rate_in,
                'Rolling_3M_Avg': rolling_3m,
                'Rolling_6M_Avg': rolling_3m,
                'Rolling_12M_Avg': prev_yr_rate_in
            }
            res = predict_single(input_dict, bundle)
            st.session_state['last_prediction'] = res
        else:
            res = st.session_state['last_prediction']
            
        st.markdown("---")
        st.markdown("### 🎯 Model Prediction Results")
        
        pred_val = res['predicted_rate']
        trend_label = res['trend']
        trend_icon = "📈" if trend_label == "Increasing" else ("📉" if trend_label == "Decreasing" else "➡️")
        
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-left: 6px solid #38BDF8; padding: 24px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="margin:0; color:#94A3B8; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">FORECASTED CRIME RATE</h4>
                <h1 style="margin: 10px 0; color:#F8FAFC; font-size: 48px; font-weight: 800;">{pred_val:.1f}</h1>
                <p style="margin:0; color:#38BDF8; font-weight: 600; font-size: 14px;">incidents per 100,000 residents</p>
            </div>
            """, unsafe_allow_html=True)
            
        with res_col2:
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                <div style="background: #0F172A; border: 1px solid #334155; border-radius: 10px; padding: 14px 16px;">
                    <div style="color: #94A3B8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">HISTORICAL AVERAGE RATE</div>
                    <div style="color: #F8FAFC; font-size: 28px; font-weight: 800; margin-top: 4px;">{res['historical_avg']:.1f}</div>
                </div>
                <div style="background: #0F172A; border: 1px solid #334155; border-radius: 10px; padding: 14px 16px;">
                    <div style="color: #94A3B8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">CHANGE FROM AVERAGE</div>
                    <div style="color: #38BDF8; font-size: 28px; font-weight: 800; margin-top: 4px;">{res['pct_change']:+.1f}%</div>
                </div>
                <div style="background: #0F172A; border: 1px solid #334155; border-radius: 10px; padding: 14px 16px;">
                    <div style="color: #94A3B8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">PREDICTED TREND</div>
                    <div style="color: #F8FAFC; font-size: 22px; font-weight: 800; margin-top: 4px;">{trend_icon} {trend_label}</div>
                </div>
                <div style="background: #0F172A; border: 1px solid #334155; border-radius: 10px; padding: 14px 16px;">
                    <div style="color: #94A3B8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">ALGORITHM USED</div>
                    <div style="color: #F8FAFC; font-size: 17px; font-weight: 800; margin-top: 6px;">{res['model_name']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #0F172A; border-left: 4px solid #38BDF8; border-radius: 8px; padding: 14px 18px; margin-top: 20px; border: 1px solid #1E293B;">
            <span style="color: #38BDF8; font-weight: 700; font-size: 14px;">ℹ️ Interpretation Note:</span>
            <span style="color: #F8FAFC; font-size: 14px; line-height: 1.5;"> This estimate reflects aggregate statistical probabilities calculated from temporal lag patterns and demographics. It does not measure individual risk.</span>
        </div>
        """, unsafe_allow_html=True)
