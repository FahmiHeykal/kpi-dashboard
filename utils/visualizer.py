import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def generate_visualizations(df, kpi_dict):
    figures = {}
    
    df_monthly = df.set_index('date').resample('M').agg({
        'revenue': 'sum',
        'cost': 'sum',
        'customer_id': 'nunique',
        'performance_score': 'mean'
    }).reset_index()
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df_monthly['date'], y=df_monthly['revenue'], 
                                 mode='lines+markers', name='Revenue', line=dict(color='#1f77b4')))
    fig_trend.add_trace(go.Scatter(x=df_monthly['date'], y=df_monthly['cost'], 
                                 mode='lines+markers', name='Cost', line=dict(color='#ff7f0e')))
    fig_trend.update_layout(title='Trend Revenue vs Cost', xaxis_title='Date', yaxis_title='Amount')
    figures['trend'] = fig_trend
    
    division_data = df.groupby('division').agg({
        'revenue': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    
    fig_pie = px.pie(division_data, values='revenue', names='division', 
                     title='Revenue Distribution by Division')
    figures['revenue_pie'] = fig_pie
    
    fig_area = px.area(df_monthly, x='date', y=['revenue', 'cost'], 
                      title='Revenue & Cost Area Chart')
    figures['area_chart'] = fig_area
    
    performance_data = df.groupby('division')['performance_score'].mean().reset_index()
    fig_bar = px.bar(performance_data, x='division', y='performance_score',
                    title='Average Performance Score by Division')
    figures['performance_bar'] = fig_bar
    
    monthly_customers = df.set_index('date').resample('M')['customer_id'].nunique().reset_index()
    fig_customers = px.line(monthly_customers, x='date', y='customer_id',
                          title='Monthly Customer Growth')
    figures['customer_growth'] = fig_customers
    
    return figures