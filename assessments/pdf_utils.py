from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import os


def render_to_pdf(template_src, context_dict={}):
    """Convert HTML template to PDF"""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    
    # Configure xhtml2pdf
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")), 
        result,
        encoding='UTF-8',
        link_callback=link_callback
    )
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def link_callback(uri, rel):
    """Handle static files in PDF"""
    if uri.startswith('http'):
        return uri
    
    # Handle static files
    if uri.startswith('/static/'):
        path = os.path.join(settings.STATIC_ROOT, uri.replace('/static/', ''))
        if os.path.exists(path):
            return path
        path = os.path.join(settings.BASE_DIR, 'static', uri.replace('/static/', ''))
        if os.path.exists(path):
            return path
        return uri
    
    return uri