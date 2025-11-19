import streamlit as st
import pandas as pd
from utils.export_handler import export_report, export_png
from utils.visualizer import generate_visualizations
from utils.kpi_calculator import calculate_kpi

def render_export_report():
    st.title("📤 Export Reports & Charts")
    
    if 'processed_data' not in st.session_state:
        st.warning("Please upload data in the main page first")
        return
    
    df = st.session_state.processed_data
    kpi_dict, _ = calculate_kpi(df)
    figures = generate_visualizations(df, kpi_dict)
    
    st.subheader("Export Charts as PNG")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Trend Chart"):
            filepath = export_png(figures['trend'], "trend_chart")
            if filepath:
                st.success(f"Chart exported: {filepath}")
    
    with col2:
        if st.button("Export Revenue Pie Chart"):
            filepath = export_png(figures['revenue_pie'], "revenue_pie")
            if filepath:
                st.success(f"Chart exported: {filepath}")
    
    with col3:
        if st.button("Export Performance Chart"):
            filepath = export_png(figures['performance_bar'], "performance_bar")
            if filepath:
                st.success(f"Chart exported: {filepath}")
    
    st.subheader("Export Reports")
    
    report_format = st.selectbox("Select Report Format", ["Excel", "CSV", "PDF"])
    
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            filepath = export_report(df, kpi_dict, report_format.lower())
            
            if filepath:
                st.success(f"Report generated: {filepath}")
                
                with open(filepath, "rb") as file:
                    btn = st.download_button(
                        label=f"Download {report_format} Report",
                        data=file,
                        file_name=filepath.split("/")[-1],
                        mime="application/octet-stream"
                    )
    
    st.subheader("Data Preview")
    st.dataframe(df.head(100), use_container_width=True)
    
    st.subheader("KPI Summary")
    kpi_df = pd.DataFrame([kpi_dict])
    st.dataframe(kpi_df, use_container_width=True)