# app/report.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .db import get_connection
from datetime import datetime
from io import BytesIO

def generate_report():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch correlation data
    cursor.execute("""
        SELECT id, timestamp, event
        FROM correlations
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    report_items = [
        {"id": row["id"], "timestamp": row["timestamp"], "event": row["event"]}
        for row in rows
    ]

    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    # Title and metadata
    elements.append(Paragraph("TOR Correlation Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated on: {datetime.now().isoformat()}", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total correlations: {len(report_items)}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table
    data = [["ID", "Timestamp", "Event"]]
    for item in report_items:
        data.append([item["id"], item["timestamp"], item["event"]])

    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return buffer  # Return in-memory PDF
