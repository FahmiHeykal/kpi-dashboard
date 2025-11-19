import streamlit as st
import pandas as pd
import yaml
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title="KPI Dashboard & OKR Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_config():
    try:
        with open('config/settings.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        st.error("❌ Config file not found. Using default settings.")
        return {
            'app_name': 'KPI Dashboard & OKR Tracker',
            'default_kpi': ['revenue', 'cost', 'profit_margin', 'customer_growth', 'churn_rate', 'employee_score'],
            'forecast': {'default_months': 6, 'min_months': 3, 'max_months': 12},
            'theme': {'default': 'light'}
        }

def main():
    try:
        config = load_config()
        app_name = config.get('app_name', 'KPI Dashboard & OKR Tracker')
        
        st.sidebar.title(f"📊 {app_name}")
        st.sidebar.markdown("---")
        
        # File upload section
        st.sidebar.subheader("📁 Data Upload")
        uploaded_file = st.sidebar.file_uploader("Upload Dataset", type=['csv', 'xlsx'])
        
        # Sample data option
        if st.sidebar.button("🎲 Use Sample Data") and os.path.exists('data/sample_data.xlsx'):
            try:
                from utils.data_loader import load_data
                from utils.preprocess import preprocess_data
                
                class MockFile:
                    name = 'sample_data.xlsx'
                
                uploaded_file = MockFile()
                st.sidebar.success("✅ Sample data loaded!")
            except Exception as e:
                st.sidebar.error(f"❌ Error loading sample data: {str(e)}")
        
        if uploaded_file is not None:
            try:
                from utils.data_loader import load_data
                from utils.preprocess import preprocess_data
                from utils.helpers import filter_data_by_date, filter_data_by_division
                
                with st.spinner("🔄 Loading and processing data..."):
                    raw_data = load_data(uploaded_file)
                    
                    if raw_data is not None:
                        processed_data = preprocess_data(raw_data)
                        st.session_state.processed_data = processed_data
                        st.sidebar.success(f"✅ Data loaded: {len(processed_data)} rows")
                        
                        # Date range filter
                        min_date = processed_data['date'].min().date()
                        max_date = processed_data['date'].max().date()
                        
                        st.sidebar.subheader("📅 Filters")
                        date_range = st.sidebar.date_input(
                            "Select Date Range",
                            value=(min_date, max_date),
                            min_value=min_date,
                            max_value=max_date
                        )
                        
                        if len(date_range) == 2:
                            start_date, end_date = date_range
                            filtered_data = filter_data_by_date(processed_data, start_date, end_date)
                            st.session_state.filtered_data = filtered_data
                        
                        # Division filter
                        divisions = st.sidebar.multiselect(
                            "Select Divisions",
                            options=sorted(processed_data['division'].unique()),
                            default=sorted(processed_data['division'].unique())
                        )
                        
                        if divisions:
                            division_data = filter_data_by_division(processed_data, divisions)
                            st.session_state.filtered_data = division_data
                    else:
                        st.sidebar.error("❌ Failed to load data")
            except Exception as e:
                st.sidebar.error(f"❌ Error processing data: {str(e)}")
        else:
            st.sidebar.info("📝 Please upload a dataset or use sample data to begin")
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("🧭 Navigation")
        
        page_options = {
            "Overview": "📊",
            "Division Analysis": "🏢", 
            "Forecast": "🔮",
            "Export Report": "📤"
        }
        
        selected_page = st.sidebar.radio("Go to", list(page_options.keys()))
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("🎨 Theme")
        theme = st.sidebar.selectbox("Select Theme", ["Light", "Dark"], index=0)
        
        # Main content area
        if 'processed_data' not in st.session_state:
            st.title("🚀 Welcome to KPI Dashboard & OKR Tracker")
            st.markdown("""
            ### Get Started:
            1. **Upload your dataset** (CSV or Excel) in the sidebar
            2. **Or use sample data** by clicking the 'Use Sample Data' button
            3. **Navigate** through different analysis pages
            
            ### Required Data Format:
            Your dataset should include these columns:
            - `date` (transaction/record date)
            - `division` (department/division name)
            - `revenue` (numeric revenue amount)
            - `cost` (numeric cost amount) 
            - `customer_id` (unique customer identifier)
            - `churn_flag` (1/0 or yes/no for customer churn)
            - `employee_id` (unique employee identifier)
            - `performance_score` (0-100 score)
            """)
            
            if st.button("📊 Generate Sample Data First"):
                try:
                    from data.sample_data_generator import generate_sample_data
                    generate_sample_data()
                    st.success("✅ Sample data generated! Click 'Use Sample Data' in sidebar.")
                except Exception as e:
                    st.error(f"❌ Error generating sample data: {str(e)}")
            
            return
        
        # Load selected page
        try:
            if selected_page == "Overview":
                from pages.Overview import render_overview
                render_overview()
            elif selected_page == "Division Analysis":
                from pages.Division_Analysis import render_division_analysis
                render_division_analysis()
            elif selected_page == "Forecast":
                from pages.Forecast import render_forecast
                render_forecast()
            elif selected_page == "Export Report":
                from pages.Export_Report import render_export_report
                render_export_report()
        except Exception as e:
            st.error(f"❌ Error loading page: {str(e)}")
            st.info("🔄 Please try uploading your data again or use sample data.")
            
    except Exception as e:
        st.error(f"❌ Application error: {str(e)}")
        st.info("🔧 Please check the requirements and try again.")

if __name__ == "__main__":
    main()