import pandas as pd

def validate_date_range(start_date, end_date):
    if start_date > end_date:
        return False, "Start date cannot be after end date"
    return True, ""

def get_division_list(df):
    return sorted(df['division'].unique().tolist())

def filter_data_by_date(df, start_date, end_date):
    return df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

def filter_data_by_division(df, divisions):
    if not divisions:
        return df
    return df[df['division'].isin(divisions)]