import streamlit as st
import plotly.express as px
import pandas as pd
from utils.kpi_calculator import calculate_kpi

def render_division_analysis():
    st.title("🏢 Division Analysis")
    
    if 'processed_data' not in st.session_state:
        st.warning("Please upload data in the main page first")
        return
    
    df = st.session_state.processed_data
    
    divisions = st.multiselect(
        "Select Divisions",
        options=sorted(df['division'].unique()),
        default=sorted(df['division'].unique())
    )
    
    if not divisions:
        st.warning("Please select at least one division")
        return
        
    filtered_df = df[df['division'].isin(divisions)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        revenue_by_division = filtered_df.groupby('division')['revenue'].sum().reset_index()
        fig_revenue = px.bar(revenue_by_division, x='division', y='revenue',
                           title="Revenue by Division")
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        customers_by_division = filtered_df.groupby('division')['customer_id'].nunique().reset_index()
        fig_customers = px.pie(customers_by_division, values='customer_id', names='division',
                             title="Customer Distribution")
        st.plotly_chart(fig_customers, use_container_width=True)
    
    performance_by_division = filtered_df.groupby('division').agg({
        'revenue': 'sum',
        'cost': 'sum',
        'customer_id': 'nunique',
        'performance_score': 'mean'
    }).reset_index()
    
    performance_by_division['profit_margin'] = ((performance_by_division['revenue'] - performance_by_division['cost']) / performance_by_division['revenue'] * 100)
    
    st.subheader("Division Performance Details")
    st.dataframe(performance_by_division, use_container_width=True)
    
    fig_scatter = px.scatter(performance_by_division, x='revenue', y='profit_margin',
                           size='customer_id', color='division',
                           title="Revenue vs Profit Margin by Division",
                           hover_data=['performance_score'])
    st.plotly_chart(fig_scatter, use_container_width=True)