"""
Utility functions for data processing and report generation.

This module contains:
1. CSV parsing and data validation using Pandas
2. Statistics calculation (averages, distributions)
3. PDF report generation with ReportLab
4. Chart generation for reports
"""

import pandas as pd
import numpy as np
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import json


def parse_csv_file(file):
    """
    Parse uploaded CSV file and return DataFrame with cleaned data.
    
    Args:
        file: Django UploadedFile object
    
    Returns:
        tuple: (pandas.DataFrame, dict with metadata)
    
    Raises:
        ValueError: If CSV is invalid or missing required columns
    """
    try:
        # Read CSV content
        content = file.read().decode('utf-8')
        df = pd.read_csv(StringIO(content))
        
        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()
        
        # Fill missing values with appropriate defaults
        # For numeric columns, use mean
        numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col].fillna(df[col].mean(), inplace=True)
        
        # For string columns, use 'Unknown'
        string_cols = ['Equipment_Name', 'Type']
        for col in string_cols:
            if col in df.columns:
                df[col].fillna('Unknown', inplace=True)
        
        # Create metadata
        metadata = {
            'total_rows': len(df),
            'columns': list(df.columns),
            'file_size': file.size,
            'file_name': file.name,
        }
        
        return df, metadata
        
    except Exception as e:
        raise ValueError(f"Error parsing CSV file: {str(e)}")


def calculate_statistics(df):
    """
    Calculate summary statistics from DataFrame.
    
    Args:
        df: pandas.DataFrame with equipment data
    
    Returns:
        dict: Statistics including counts, averages, and distribution
    """
    stats = {
        'total_equipment': len(df),
        'avg_flowrate': float(df['Flowrate'].mean()) if 'Flowrate' in df.columns else None,
        'avg_pressure': float(df['Pressure'].mean()) if 'Pressure' in df.columns else None,
        'avg_temperature': float(df['Temperature'].mean()) if 'Temperature' in df.columns else None,
    }
    
    # Calculate equipment type distribution
    if 'Type' in df.columns:
        type_counts = df['Type'].value_counts().to_dict()
        stats['equipment_distribution'] = type_counts
    else:
        stats['equipment_distribution'] = {}
    
    return stats


def dataframe_to_json(df):
    """
    Convert DataFrame to JSON-serializable list of dictionaries.
    
    Args:
        df: pandas.DataFrame
    
    Returns:
        list: List of dictionaries representing rows
    """
    # Replace NaN with None for JSON serialization
    df_clean = df.replace({np.nan: None})
    return df_clean.to_dict('records')


def create_bar_chart(data_dict, title="Equipment Distribution"):
    """
    Create a bar chart drawing for ReportLab.
    
    Args:
        data_dict: Dictionary with labels and values
        title: Chart title
    
    Returns:
        Drawing object
    """
    drawing = Drawing(400, 200)
    
    # Prepare data
    labels = list(data_dict.keys())[:10]  # Limit to 10 categories
    values = [data_dict[k] for k in labels]
    
    # Create bar chart
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = [values]
    bc.categoryAxis.categoryNames = labels
    bc.categoryAxis.labels.angle = 45
    bc.categoryAxis.labels.fontSize = 8
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max(values) * 1.2 if values else 10
    
    # Styling
    bc.bars[0].fillColor = colors.HexColor('#4A90E2')
    bc.valueAxis.labels.fontSize = 8
    
    drawing.add(bc)
    return drawing


def create_pie_chart(data_dict, title="Distribution"):
    """
    Create a pie chart drawing for ReportLab.
    
    Args:
        data_dict: Dictionary with labels and values
        title: Chart title
    
    Returns:
        Drawing object
    """
    drawing = Drawing(400, 200)
    
    # Prepare data
    labels = list(data_dict.keys())[:8]  # Limit to 8 slices
    values = [data_dict[k] for k in labels]
    
    # Create pie chart
    pie = Pie()
    pie.x = 150
    pie.y = 50
    pie.width = 120
    pie.height = 120
    pie.data = values
    pie.labels = labels
    pie.slices.strokeWidth = 0.5
    pie.slices.fontSize = 8
    
    # Color scheme
    colors_list = [
        colors.HexColor('#4A90E2'),
        colors.HexColor('#50C878'),
        colors.HexColor('#FFB347'),
        colors.HexColor('#FF6B6B'),
        colors.HexColor('#9B59B6'),
        colors.HexColor('#3498DB'),
        colors.HexColor('#E74C3C'),
        colors.HexColor('#F39C12'),
    ]
    
    for i, color in enumerate(colors_list[:len(values)]):
        pie.slices[i].fillColor = color
    
    drawing.add(pie)
    return drawing


def generate_pdf_report(dataset):
    """
    Generate a comprehensive PDF report for a dataset.
    
    Args:
        dataset: Dataset model instance
    
    Returns:
        BytesIO: PDF file content
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Chemical Equipment Analysis Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Metadata section
    metadata_heading = Paragraph("Dataset Information", heading_style)
    elements.append(metadata_heading)
    
    metadata_data = [
        ['Dataset Name:', dataset.name],
        ['Upload Date:', dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')],
        ['Total Equipment:', str(dataset.total_equipment)],
        ['Uploaded By:', dataset.user.username],
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(metadata_table)
    elements.append(Spacer(1, 20))
    
    # Summary Statistics
    stats_heading = Paragraph("Summary Statistics", heading_style)
    elements.append(stats_heading)
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(dataset.total_equipment)],
        ['Average Flowrate', f"{dataset.avg_flowrate:.2f}" if dataset.avg_flowrate else 'N/A'],
        ['Average Pressure', f"{dataset.avg_pressure:.2f}" if dataset.avg_pressure else 'N/A'],
        ['Average Temperature', f"{dataset.avg_temperature:.2f}" if dataset.avg_temperature else 'N/A'],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 20))
    
    # Equipment Distribution
    if dataset.equipment_distribution:
        dist_heading = Paragraph("Equipment Type Distribution", heading_style)
        elements.append(dist_heading)
        
        # Distribution table
        dist_data = [['Equipment Type', 'Count', 'Percentage']]
        total = sum(dataset.equipment_distribution.values())
        
        for eq_type, count in sorted(dataset.equipment_distribution.items(), 
                                      key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            dist_data.append([eq_type, str(count), f"{percentage:.1f}%"])
        
        dist_table = Table(dist_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E8F8F5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
        ]))
        elements.append(dist_table)
        elements.append(Spacer(1, 20))
        
        # Add bar chart
        elements.append(Paragraph("Visual Distribution", heading_style))
        bar_chart = create_bar_chart(dataset.equipment_distribution)
        elements.append(bar_chart)
        elements.append(Spacer(1, 20))
    
    # Data preview (first 10 rows)
    if dataset.data_json:
        preview_heading = Paragraph("Data Preview (First 10 Records)", heading_style)
        elements.append(preview_heading)
        
        preview_data = [['Equipment', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        
        data_list = dataset.data_json[:10] if isinstance(dataset.data_json, list) else []
        
        for record in data_list:
            preview_data.append([
                str(record.get('Equipment_Name', 'N/A'))[:20],
                str(record.get('Type', 'N/A'))[:15],
                f"{record.get('Flowrate', 0):.1f}",
                f"{record.get('Pressure', 0):.1f}",
                f"{record.get('Temperature', 0):.1f}",
            ])
        
        preview_table = Table(preview_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 1*inch, 1*inch])
        preview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
        ]))
        elements.append(preview_table)
    
    # Footer
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Chemical Equipment Visualizer"
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF content
    buffer.seek(0)
    return buffer