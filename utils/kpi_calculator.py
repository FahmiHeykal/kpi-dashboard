import pandas as pd
import numpy as np

def calculate_kpi(df):
    kpi_dict = {}
    
    kpi_dict['revenue'] = df['revenue'].sum()
    kpi_dict['cost'] = df['cost'].sum()
    kpi_dict['profit_margin'] = ((kpi_dict['revenue'] - kpi_dict['cost']) / kpi_dict['revenue'] * 100) if kpi_dict['revenue'] > 0 else 0
    
    unique_customers = df['customer_id'].nunique()
    kpi_dict['customer_growth'] = unique_customers
    
    churned_customers = df[df['churn_flag'] == 1]['customer_id'].nunique()
    kpi_dict['churn_rate'] = (churned_customers / unique_customers * 100) if unique_customers > 0 else 0
    
    kpi_dict['employee_score'] = df['performance_score'].mean()
    
    df_monthly = df.set_index('date').resample('M').agg({
        'revenue': 'sum',
        'cost': 'sum',
        'customer_id': 'nunique',
        'performance_score': 'mean'
    }).reset_index()
    
    if len(df_monthly) > 1:
        kpi_dict['mom'] = {
            'revenue': ((df_monthly['revenue'].iloc[-1] - df_monthly['revenue'].iloc[-2]) / df_monthly['revenue'].iloc[-2] * 100) if df_monthly['revenue'].iloc[-2] > 0 else 0,
            'customer_growth': ((df_monthly['customer_id'].iloc[-1] - df_monthly['customer_id'].iloc[-2]) / df_monthly['customer_id'].iloc[-2] * 100) if df_monthly['customer_id'].iloc[-2] > 0 else 0
        }
    else:
        kpi_dict['mom'] = {'revenue': 0, 'customer_growth': 0}
    
    df_yearly = df.copy()
    df_yearly['year'] = df_yearly['date'].dt.year
    yearly_agg = df_yearly.groupby('year').agg({
        'revenue': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    
    if len(yearly_agg) > 1:
        kpi_dict['yoy'] = {
            'revenue': ((yearly_agg['revenue'].iloc[-1] - yearly_agg['revenue'].iloc[-2]) / yearly_agg['revenue'].iloc[-2] * 100) if yearly_agg['revenue'].iloc[-2] > 0 else 0,
            'customer_growth': ((yearly_agg['customer_id'].iloc[-1] - yearly_agg['customer_id'].iloc[-2]) / yearly_agg['customer_id'].iloc[-2] * 100) if yearly_agg['customer_id'].iloc[-2] > 0 else 0
        }
    else:
        kpi_dict['yoy'] = {'revenue': 0, 'customer_growth': 0}
    
    aggregated_df = df.groupby('division').agg({
        'revenue': 'sum',
        'cost': 'sum',
        'customer_id': 'nunique',
        'churn_flag': 'sum',
        'performance_score': 'mean'
    }).reset_index()
    
    aggregated_df['profit_margin'] = ((aggregated_df['revenue'] - aggregated_df['cost']) / aggregated_df['revenue'] * 100)
    aggregated_df['churn_rate'] = (aggregated_df['churn_flag'] / aggregated_df['customer_id'] * 100)
    
    return kpi_dict, aggregated_df