import streamlit as st
import pandas as pd
from utils.model import train_and_evaluate_models, load_model_bundle
from utils.feature_engineering import create_features
from utils.visualization import plot_actual_vs_predicted, plot_feature_importance

def render_model_performance_page():
    st.markdown("## 🔬 Model Performance & Algorithm Evaluation")
    st.markdown("Evaluate predictive accuracy metrics and compare Machine Learning algorithms on chronological test data.")
    
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

    st.markdown("### ⚙️ Train & Re-evaluate Models")
    if st.button("🚀 Train / Re-evaluate ML Models", type="primary"):
        with st.spinner("Engineering time lag features and fitting Random Forest & Linear Regression models..."):
            df_feat = create_features(df_cleaned)
            eval_res = train_and_evaluate_models(df_feat)
            st.session_state['eval_res'] = eval_res
            st.success("Models trained and evaluated successfully!")

    eval_res = st.session_state.get('eval_res', None)
    if eval_res is None:
        try:
            df_feat = create_features(df_cleaned)
            eval_res = train_and_evaluate_models(df_feat)
            st.session_state['eval_res'] = eval_res
        except Exception as e:
            st.error(f"Failed to evaluate models: {e}")
            return

    rf_m = eval_res['rf_metrics']
    lr_m = eval_res['lr_metrics']
    
    st.markdown("---")
    st.markdown("### 🏆 Algorithm Performance Comparison")
    
    comp_df = pd.DataFrame([
        {
            'Algorithm': 'Model 1: Linear Regression',
            'Mean Absolute Error (MAE)': lr_m['MAE'],
            'Root Mean Squared Error (RMSE)': lr_m['RMSE'],
            'R² Score': lr_m['R2']
        },
        {
            'Algorithm': 'Model 2: Random Forest Regressor (Selected)',
            'Mean Absolute Error (MAE)': rf_m['MAE'],
            'Root Mean Squared Error (RMSE)': rf_m['RMSE'],
            'R² Score': rf_m['R2']
        }
    ])
    
    st.table(comp_df)
    
    st.info(f"📊 **Evaluation Details:** Evaluated on chronological test set containing **{eval_res['test_size']:,}** records out of **{eval_res['dataset_size']:,}** total observations (80/20 train-test split).")
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📈 Actual vs Predicted Crime Rate")
        st.plotly_chart(plot_actual_vs_predicted(eval_res['y_test'][:100], eval_res['y_pred_rf'][:100]))
        
    with c2:
        st.markdown("### 🌳 Feature Importance (Random Forest)")
        st.plotly_chart(plot_feature_importance(eval_res['importances']))
        st.caption("> 💡 **Feature Importance Explanation:** Feature importance shows which input variables were most useful to the Random Forest model during decision tree splits. It does not imply direct physical causality.")
