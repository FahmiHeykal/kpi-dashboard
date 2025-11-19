import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def generate_forecast(df, column='revenue', months=6):
    try:
        df_monthly = df.set_index('date').resample('M')[column].sum().reset_index()
        
        if len(df_monthly) < 3:
            return None, None
            
        df_monthly['month_index'] = range(len(df_monthly))
        
        X = df_monthly[['month_index']].values
        y = df_monthly[column].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        future_months = list(range(len(df_monthly), len(df_monthly) + months))
        X_future = np.array(future_months).reshape(-1, 1)
        
        predictions = model.predict(X_future)
        
        last_date = df_monthly['date'].max()
        future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=months, freq='M')
        
        predict_df = pd.DataFrame({
            'date': future_dates,
            'predicted': predictions,
            'type': 'forecast'
        })
        
        actual_df = pd.DataFrame({
            'date': df_monthly['date'],
            'predicted': y,
            'type': 'actual'
        })
        
        combined_df = pd.concat([actual_df, predict_df], ignore_index=True)
        
        return combined_df, model
        
    except Exception as e:
        print(f"Forecast error: {str(e)}")
        return None, None