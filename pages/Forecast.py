import streamlit as st
import pandas as pd
from utils.forecast_model import generate_forecast
import plotly.graph_objects as go

def render_forecast():
    st.title("🔮 Revenue Forecast")
    
    if 'processed_data' not in st.session_state:
        st.warning("Please upload data in the main page first")
        return
    
    df = st.session_state.processed_data
    
    months = st.slider("Forecast Months", min_value=3, max_value=12, value=6)
    
    forecast_df, model = generate_forecast(df, 'revenue', months)
    
    if forecast_df is not None and model is not None:
        fig = go.Figure()
        
        actual_data = forecast_df[forecast_df['type'] == 'actual']
        forecast_data = forecast_df[forecast_df['type'] == 'forecast']
        
        fig.add_trace(go.Scatter(x=actual_data['date'], y=actual_data['predicted'],
                               mode='lines+markers', name='Actual', line=dict(color='blue')))
        
        fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['predicted'],
                               mode='lines+markers', name='Forecast', line=dict(color='red', dash='dash')))
        
        fig.update_layout(title='Revenue Forecast', xaxis_title='Date', yaxis_title='Revenue')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Forecast Details")
        st.dataframe(forecast_data[['date', 'predicted']].rename(columns={'predicted': 'forecasted_revenue'}), use_container_width=True)
        
        last_actual = actual_data['predicted'].iloc[-1] if not actual_data.empty else 0
        total_forecast = forecast_data['predicted'].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Last Actual Revenue", f"${last_actual:,.2f}")
        with col2:
            st.metric("Total Forecasted Revenue", f"${total_forecast:,.2f}")
    else:
        st.error("Insufficient data for forecasting. Need at least 3 months of historical data.")