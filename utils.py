"""
Utility functions for the Crafted Journeys application
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def generate_receipt_pdf(payment):
    """
    Generate a PDF receipt for a payment
    
    Args:
        payment: Payment model instance
        
    Returns:
        BytesIO object containing the PDF
    """
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF object using the buffer as its "file"
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        title=f"Receipt #{payment.id} - Crafted Journeys"
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Define custom styles
    styles.add(ParagraphStyle(
        name='CenteredTitle',
        parent=styles['Heading1'],
        alignment=1,  # 0=left, 1=center, 2=right
        spaceAfter=20
    ))
    
    styles.add(ParagraphStyle(
        name='RightAligned',
        parent=styles['Normal'],
        alignment=2,  # 0=left, 1=center, 2=right
    ))
    
    # Add company logo and title
    elements.append(Image("static/assets/openart-image_fJzOJQBm_1742026809050_raw.jpg", width=6*cm, height=2*cm))
    elements.append(Paragraph("Crafted Journeys", styles['CenteredTitle']))
    elements.append(Paragraph("Payment Receipt", styles['CenteredTitle']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Payment Information Table
    payment_data = [
        ["Receipt Number:", f"#{payment.id}"],
        ["Date:", payment.formatted_date()],
        ["Transaction ID:", payment.stripe_payment_id or "N/A"],
        ["Status:", payment.status.upper()],
    ]
    
    payment_table = Table(payment_data, colWidths=[doc.width/3, doc.width*2/3])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(payment_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Customer Information
    elements.append(Paragraph("Customer Information", styles['Heading2']))
    elements.append(Spacer(1, 0.25*cm))
    
    customer_data = [
        ["Name:", payment.user.username],
        ["Email:", payment.user.email],
    ]
    
    customer_table = Table(customer_data, colWidths=[doc.width/3, doc.width*2/3])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(customer_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Package Details
    elements.append(Paragraph("Package Details", styles['Heading2']))
    elements.append(Spacer(1, 0.25*cm))
    
    package_data = [
        ["Package:", payment.package.name],
        ["Destination:", payment.package.location.name],
        ["Category:", payment.package.category],
        ["Duration:", f"{payment.package.duration} days"],
    ]
    
    package_table = Table(package_data, colWidths=[doc.width/3, doc.width*2/3])
    package_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(package_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Payment Details
    elements.append(Paragraph("Payment Details", styles['Heading2']))
    elements.append(Spacer(1, 0.25*cm))
    
    # Define the payment details table
    payment_details = [
        ["Item", "Amount"],
        ["Package Price", f"{payment.currency} {payment.amount / 1.18:.2f}"],
        ["GST (18%)", f"{payment.currency} {payment.amount * 0.18 / 1.18:.2f}"],
        ["Total", payment.formatted_amount()],
    ]
    
    payment_details_table = Table(payment_details, colWidths=[doc.width/2, doc.width/2])
    payment_details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(payment_details_table)
    elements.append(Spacer(1, 1*cm))
    
    # Terms and conditions
    elements.append(Paragraph("Terms and Conditions", styles['Heading3']))
    elements.append(Spacer(1, 0.25*cm))
    terms_text = """
    1. This receipt is evidence of full payment for the above package.
    2. Cancellation policy: Refunds available up to 30 days before scheduled departure.
    3. Package modifications are subject to availability and may incur additional charges.
    4. For any queries regarding this payment, please contact support@craftedjourneys.com.
    """
    elements.append(Paragraph(terms_text, styles['Normal']))
    
    # Add footer with contact information
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("Crafted Journeys - 123 Travel Street, New Delhi, India", styles['RightAligned']))
    elements.append(Paragraph("Phone: +91 1234567890 | Email: info@craftedjourneys.com", styles['RightAligned']))
    elements.append(Paragraph("www.craftedjourneys.com", styles['RightAligned']))
    
    # Build the PDF
    doc.build(elements)
    
    # File position is at the end of the file
    buffer.seek(0)
    return buffer
