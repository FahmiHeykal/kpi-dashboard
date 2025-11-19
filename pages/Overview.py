import streamlit as st
import pandas as pd
from utils.kpi_calculator import calculate_kpi
from utils.visualizer import generate_visualizations
from utils.formatter import format_currency, format_percentage, format_number

def render_overview():
    st.title("📊 KPI Overview Dashboard")
    
    if 'processed_data' not in st.session_state:
        st.warning("Please upload data in the main page first")
        return
    
    df = st.session_state.processed_data
    
    st.subheader("Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", format_currency(df['revenue'].sum()))
    with col2:
        st.metric("Total Cost", format_currency(df['cost'].sum()))
    with col3:
        profit = df['revenue'].sum() - df['cost'].sum()
        st.metric("Total Profit", format_currency(profit))
    with col4:
        st.metric("Unique Customers", format_number(df['customer_id'].nunique()))
    
    kpi_dict, aggregated_df = calculate_kpi(df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Profit Margin", 
                 format_percentage(kpi_dict['profit_margin']))
    with col2:
        st.metric("Churn Rate", 
                 format_percentage(kpi_dict['churn_rate']))
    with col3:
        st.metric("Employee Score", 
                 f"{kpi_dict['employee_score']:.1f}")
    
    st.subheader("Performance Trends")
    
    figures = generate_visualizations(df, kpi_dict)
    
    for fig_name, fig in figures.items():
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Division Performance Summary")
    st.dataframe(aggregated_df, use_container_width=True)