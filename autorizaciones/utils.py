import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generar_pdf_autorizacion(autorizacion):
    # Crear carpeta si no existe
    carpeta_pdf = os.path.join(settings.MEDIA_ROOT, 'autorizaciones_pdf')
    os.makedirs(carpeta_pdf, exist_ok=True)

    # Ruta final del archivo
    ruta = os.path.join(carpeta_pdf, f'autorizacion_{autorizacion.id}.pdf')

    # Crear el PDF
    c = canvas.Canvas(ruta, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Autorización de Retiro de EPP")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Nombre Trabajador: {autorizacion.nombre_trabajador}")
    c.drawString(50, height - 120, f"RUT: {autorizacion.rut_trabajador}")
    c.drawString(50, height - 140, f"Personal de Bodega: {autorizacion.personal_bodega}")
    c.drawString(50, height - 160, f"Fecha: {autorizacion.fecha.strftime('%d-%m-%Y %H:%M')}")

    c.drawString(50, height - 200, "EPP Solicitado:")
    epps = autorizacion.epp_solicitado.split(', ')
    y = height - 220
    for epp in epps:
        c.drawString(70, y, f"- {epp}")
        y -= 20

    c.showPage()
    c.save()