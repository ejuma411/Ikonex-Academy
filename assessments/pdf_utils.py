from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from django.conf import settings
import os


def render_to_pdf(template_src, context_dict={}):
    """
    Convert data to PDF using ReportLab
    Note: This is a placeholder. Use ProfessionalReportPDF class instead.
    """
    # This is just a placeholder - use ProfessionalReportPDF for actual PDF generation
    from .pdf_generator import ProfessionalReportPDF
    
    # You would need to extract data from context_dict and pass to ProfessionalReportPDF
    # For now, return None as we're using the dedicated PDF generator
    return None


def link_callback(uri, rel):
    """Handle static files in PDF (for potential future use)"""
    if uri.startswith('http'):
        return uri
    
    if uri.startswith('/static/'):
        path = os.path.join(settings.STATIC_ROOT, uri.replace('/static/', ''))
        if os.path.exists(path):
            return path
        path = os.path.join(settings.BASE_DIR, 'static', uri.replace('/static/', ''))
        if os.path.exists(path):
            return path
        return uri
    
    return uri