import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def export_csv(queryset, fields, filename='report.csv'):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(fields)  # Header

    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        writer.writerow(row)

    return response

def export_pdf(template_src, context_dict, filename="report.pdf"):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF <pre>" + html + "</pre>")
    return response

import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# -----------------------------
# CSV Export
# -----------------------------
def export_csv(queryset, fields, filename='report.csv'):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(fields)  # Header

    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        writer.writerow(row)

    return response

# -----------------------------
# PDF Export
# -----------------------------
def export_pdf(template_src, context_dict, filename="report.pdf"):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF <pre>" + html + "</pre>")
    return response
import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# -----------------------------
# CSV Export
# -----------------------------
def export_csv(queryset, fields, filename='report.csv'):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(fields)  # Header

    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        writer.writerow(row)

    return response

# -----------------------------
# PDF Export
# -----------------------------
def export_pdf(template_src, context_dict, filename="report.pdf"):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF <pre>" + html + "</pre>")
    return response
