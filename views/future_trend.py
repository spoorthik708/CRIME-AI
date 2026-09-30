import streamlit as st
import pandas as pd
from utils.visualization import plot_future_trend
from utils.model import load_model_bundle, predict_single

def render_future_trend_page():
    st.markdown("## 📈 Multi-Year Future Crime Trend Projection")
    st.markdown("Project future crime rate trajectories across Indian cities by combining historical baseline trends with machine learning regression predictions.")
    
    df_cleaned = st.session_state.get('df_cleaned', None)
    if df_cleaned is None:
        try:
            from utils.data_processing import clean_data
            raw = st.session_state.get('df_raw', pd.read_csv("data/sample_data.csv"))
            df_cleaned, _ = clean_data(raw)
            st.session_state['df_cleaned'] = df_cleaned
        except Exception:
            st.warning("Please load dataset first.")
            return

    # Historical yearly average
    hist_yearly = df_cleaned.groupby('Year')['Crime_Rate'].mean().reset_index()
    hist_yearly['Status'] = 'Historical Data'
    
    last_year = int(hist_yearly['Year'].max())
    last_rate = float(hist_yearly.loc[hist_yearly['Year'] == last_year, 'Crime_Rate'].values[0])
    
    bundle = load_model_bundle()
    
    future_years = [last_year + 1, last_year + 2, last_year + 3]
    future_rows = []
    
    curr_rate = last_rate
    for yr in future_years:
        if bundle is not None:
            inp = {
                'Year': yr,
                'Month': 6,
                'Population': int(df_cleaned['Population'].mean()),
                'Previous_Crime_Rate': curr_rate,
                'Previous_Year_Crime_Rate': curr_rate * 0.98,
                'Previous_Month_Crime_Rate': curr_rate,
                'Rolling_3M_Avg': curr_rate,
                'Rolling_6M_Avg': curr_rate,
                'Rolling_12M_Avg': curr_rate
            }
            res = predict_single(inp, bundle)
            pred_rate = res['predicted_rate']
        else:
            pred_rate = round(curr_rate * 1.025, 2)
            
        future_rows.append({'Year': yr, 'Crime_Rate': pred_rate, 'Status': 'Predicted Data'})
        curr_rate = pred_rate
        
    future_df = pd.DataFrame(future_rows)
    
    st.markdown("---")
    st.plotly_chart(plot_future_trend(hist_yearly, future_df))
    
    st.markdown("---")
    st.markdown("### 📊 Historical vs Projected Crime Rate Table")
    
    full_table = pd.concat([hist_yearly, future_df], ignore_index=True)
    full_table['Crime_Rate'] = full_table['Crime_Rate'].round(2)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.dataframe(full_table)
        
    with c2:
        st.markdown("#### Key Projection Metrics")
        st.metric("Latest Historical Rate", f"{last_rate:.1f}")
        st.metric(f"Projected Rate ({future_years[0]})", f"{future_df.iloc[0]['Crime_Rate']:.1f}")
        pct_diff = ((future_df.iloc[-1]['Crime_Rate'] - last_rate) / last_rate) * 100.0
        st.metric("Projected 3-Year Change", f"{pct_diff:+.1f}%")
