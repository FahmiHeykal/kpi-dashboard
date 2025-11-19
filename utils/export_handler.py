import pandas as pd
import plotly.io as pio
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tempfile

def export_png(fig, filename=None):
    try:
        os.makedirs('export/charts', exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chart_{timestamp}.png"
        else:
            filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        filepath = os.path.join('export/charts', filename)
        pio.write_image(fig, filepath)
        
        return filepath
    except Exception as e:
        print(f"Export PNG error: {str(e)}")
        return None

def export_report(df, kpi_dict, format_type='excel'):
    try:
        os.makedirs('export/reports', exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == 'excel':
            filename = f"kpi_report_{timestamp}.xlsx"
            filepath = os.path.join('export/reports', filename)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Raw Data', index=False)
                
                kpi_summary = pd.DataFrame([kpi_dict])
                kpi_summary.to_excel(writer, sheet_name='KPI Summary', index=False)
                
            return filepath
            
        elif format_type == 'csv':
            filename = f"kpi_report_{timestamp}.csv"
            filepath = os.path.join('export/reports', filename)
            df.to_csv(filepath, index=False)
            return filepath
            
        elif format_type == 'pdf':
            filename = f"kpi_report_{timestamp}.pdf"
            filepath = os.path.join('export/reports', filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph("KPI Dashboard Report", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            date_info = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
            story.append(date_info)
            story.append(Spacer(1, 12))
            
            period_info = Paragraph(f"Data Period: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}", styles['Normal'])
            story.append(period_info)
            story.append(Spacer(1, 12))
            
            kpi_data = [
                ['KPI', 'Value'],
                ['Revenue', f"${kpi_dict.get('revenue', 0):,.2f}"],
                ['Cost', f"${kpi_dict.get('cost', 0):,.2f}"],
                ['Profit Margin', f"{kpi_dict.get('profit_margin', 0):.2f}%"],
                ['Customer Growth', f"{kpi_dict.get('customer_growth', 0):,}"],
                ['Churn Rate', f"{kpi_dict.get('churn_rate', 0):.2f}%"],
                ['Employee Score', f"{kpi_dict.get('employee_score', 0):.2f}"]
            ]
            
            kpi_table = Table(kpi_data)
            kpi_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(kpi_table)
            story.append(Spacer(1, 20))
            
            doc.build(story)
            return filepath
            
    except Exception as e:
        print(f"Export report error: {str(e)}")
        return None