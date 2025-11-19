import pandas as pd
import numpy as np
import streamlit as st

def preprocess_data(df):
    try:
        df_processed = df.copy()
        
        # Convert date
        df_processed['date'] = pd.to_datetime(df_processed['date'], errors='coerce')
        df_processed = df_processed.dropna(subset=['date'])
        
        # Convert numeric columns
        df_processed['revenue'] = pd.to_numeric(df_processed['revenue'], errors='coerce')
        df_processed['cost'] = pd.to_numeric(df_processed['cost'], errors='coerce')
        df_processed['performance_score'] = pd.to_numeric(df_processed['performance_score'], errors='coerce')
        
        # Remove invalid values
        df_processed = df_processed[df_processed['revenue'] >= 0]
        df_processed = df_processed[df_processed['cost'] >= 0]
        df_processed = df_processed[(df_processed['performance_score'] >= 0) & (df_processed['performance_score'] <= 100)]
        
        # Convert churn flag
        df_processed['churn_flag'] = df_processed['churn_flag'].astype(str).str.lower().map({
            'yes': 1, 'no': 0, '1': 1, '0': 0, 'true': 1, 'false': 0, 'y': 1, 'n': 0
        }).fillna(0).astype(int)
        
        # Final cleanup
        df_processed = df_processed.dropna()
        
        st.info(f"✅ Data processed: {len(df_processed)} valid records")
        return df_processed
        
    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        return None