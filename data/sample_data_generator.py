import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data():
    print("Generating sample data...")
    
    np.random.seed(42)
    
    divisions = ['Sales', 'Marketing', 'IT', 'HR', 'Finance']
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 31)
    
    data = []
    customer_id = 1000
    employee_id = 5000
    
    current_date = start_date
    day_count = 0
    max_days = 100  # Batasi jumlah hari untuk menghindari data terlalu besar
    
    while current_date <= end_date and day_count < max_days:
        for division in divisions:
            records_per_day = np.random.randint(2, 5)
            for _ in range(records_per_day):
                revenue = np.random.uniform(1000, 20000)
                cost = revenue * np.random.uniform(0.3, 0.6)
                performance_score = np.random.uniform(70, 95)
                churn_flag = np.random.choice([0, 1], p=[0.9, 0.1])
                
                data.append({
                    'date': current_date,
                    'division': division,
                    'revenue': round(revenue, 2),
                    'cost': round(cost, 2),
                    'customer_id': f"C{customer_id}",
                    'churn_flag': churn_flag,
                    'employee_id': f"E{employee_id}",
                    'performance_score': round(performance_score, 1)
                })
                
                customer_id += 1
                employee_id += 1
        
        current_date += timedelta(days=1)
        day_count += 1
    
    df = pd.DataFrame(data)
    
    os.makedirs('data', exist_ok=True)
    df.to_excel('data/sample_data.xlsx', index=False)
    
    print("✅ Sample data generated: data/sample_data.xlsx")
    print(f"📊 Total records: {len(df)}")
    print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"🏢 Divisions: {divisions}")
    print(f"💰 Revenue range: ${df['revenue'].min():.2f} - ${df['revenue'].max():.2f}")

if __name__ == "__main__":
    generate_sample_data()