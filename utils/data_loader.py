import pandas as pd
import streamlit as st
import os

def load_data(file):
    try:
        # Handle sample data
        if hasattr(file, 'name') and file.name == 'sample_data.xlsx':
            if os.path.exists('data/sample_data.xlsx'):
                df = pd.read_excel('data/sample_data.xlsx', engine='openpyxl')
            else:
                st.error("Sample data not found. Please generate sample data first.")
                return None
        elif hasattr(file, 'name') and file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif hasattr(file, 'name') and file.name.endswith('.xlsx'):
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error("❌ Unsupported file format. Please use CSV or Excel.")
            return None
        
        required_columns = ['date', 'division', 'revenue', 'cost', 'customer_id', 'churn_flag', 'employee_id', 'performance_score']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"❌ Missing required columns: {missing_columns}")
            st.info("📋 Your dataset must include: date, division, revenue, cost, customer_id, churn_flag, employee_id, performance_score")
            return None
        
        # Basic cleaning
        df_clean = df.drop_duplicates().dropna()
        
        if df_clean.empty:
            st.error("❌ Data is empty after cleaning")
            return None
        
        st.success(f"✅ Data loaded successfully: {len(df_clean)} rows, {len(df_clean.columns)} columns")
        return df_clean
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None