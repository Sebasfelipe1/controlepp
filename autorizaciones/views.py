from django.shortcuts import render, redirect, get_object_or_404
from .forms import AutorizacionForm, EPPForm
from .models import Autorizacion, EPP
from reportlab.lib.pagesizes import LETTER
from .utils import generar_pdf_autorizacion
from django.urls import reverse
import os
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from trabajadores.models import Trabajador
from django.db.models.functions import Replace
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
import json
from autorizaciones.models import EPP
from django.http import FileResponse
from reportlab.lib.units import inch
from reportlab.lib import colors
import json, os
from .models import EPP
from datetime import datetime
import io
import io
import json
from datetime import datetime
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import Autorizacion, EPP
from django.db.models import Q
from autorizaciones.models import PerfilUsuario



@login_required
def registrar_autorizacion(request):
    rut_validado = request.session.get('rut_validado')
    trabajador_info = {}

    if rut_validado:
        try:
            trabajador = Trabajador.objects.get(rut=rut_validado)
            trabajador_info = {
                'rut': trabajador.rut,
                'nombre_completo': f"{trabajador.nombre} {trabajador.apellido_paterno} {trabajador.apellido_materno}",
                'cargo': trabajador.nombre_cargo
            }
        except Trabajador.DoesNotExist:
            trabajador_info = {}

    if request.method == 'POST':
        form = AutorizacionForm(request.POST)
        if form.is_valid():
            autorizacion = form.save(commit=False)
            autorizacion.rut_trabajador = trabajador_info.get('rut')
            autorizacion.nombre_trabajador = trabajador_info.get('nombre_completo')
            autorizacion.personal_bodega = form.cleaned_data['personal_bodega']
            autorizacion.epp_solicitado = form.cleaned_data['epp_solicitado']

            # 🔐 Asignación automática de faena
            if request.user.username.startswith("bodega_"):
                # Extrae automáticamente la faena desde el username
                autorizacion.faena = request.user.username.replace("bodega_", "").lower()
            elif request.user.username == "prevencion":
                autorizacion.faena = "prevencion"  # o dejar en blanco si no aplica
            else:
                autorizacion.faena = "admin"  # o permitir al admin seleccionarla si quieres

            autorizacion.save()
            del request.session['rut_validado']
            return redirect('vista_previa_autorizacion', id=autorizacion.id)
    else:
        form = AutorizacionForm()

    return render(request, 'autorizaciones/registrar.html', {
        'form': form,
        'trabajador_info': trabajador_info
    })
    


@login_required
def lista_autorizaciones(request):
    try:
        faena_usuario = request.user.perfilusuario.faena
        print("FAENA DETECTADA:", faena_usuario)
        autorizaciones = Autorizacion.objects.filter(faena=faena_usuario).order_by('-fecha')
    except Exception as e:
        print("ERROR O USUARIO SIN FAENA:", e)
        autorizaciones = Autorizacion.objects.all().order_by('-fecha')

    paginator = Paginator(autorizaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'autorizaciones/lista.html', {
        'page_obj': page_obj,
        'MEDIA_URL': settings.MEDIA_URL  
    })

def agregar_epp(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            EPP.objects.get_or_create(nombre=nombre.upper())
    return redirect('registrar_autorizacion')


def vista_previa_autorizacion(request, id):
    autorizacion = get_object_or_404(Autorizacion, id=id)

    try:
        epp_data = json.loads(autorizacion.epp_solicitado)
    except json.JSONDecodeError:
        epp_data = []

    epp_detalles = []
    for item in epp_data:
        try:
            epp = EPP.objects.get(id=item['id'])
            epp_detalles.append({
                'nombre': epp.nombre,
                'cantidad': item['cantidad']
            })
        except EPP.DoesNotExist:
            continue

    return render(request, 'autorizaciones/vista_previa.html', {
        'autorizacion': autorizacion,
        'epp_detalles': epp_detalles,
    })


def lista_epp(request):
    epps = EPP.objects.all()
    return render(request, 'epp/lista.html', {'epps': epps})

def agregar_epp(request):
    form = EPPForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_epp')
    return render(request, 'epp/formulario.html', {'form': form, 'accion': 'Agregar'})

def editar_epp(request, id):
    epp = get_object_or_404(EPP, id=id)
    form = EPPForm(request.POST or None, instance=epp)
    if form.is_valid():
        form.save()
        return redirect('lista_epp')
    return render(request, 'epp/formulario.html', {'form': form, 'accion': 'Editar'})

def eliminar_epp(request, id):
    epp = get_object_or_404(EPP, id=id)
    if request.method == 'POST':
        epp.delete()
        return redirect('lista_epp')
    return render(request, 'epp/eliminar.html', {'epp': epp})




def verificar_trabajador(request):
    rut = request.GET.get('rut', '').strip()
    try:
        trabajador = Trabajador.objects.get(rut__iexact=rut)
        nombre_completo = f"{trabajador.nombre} {trabajador.apellido_paterno} {trabajador.apellido_materno}"
        return JsonResponse({
            'existe': True,
            'nombre_completo': nombre_completo,
            'cargo': trabajador.nombre_cargo
        })
    except Trabajador.DoesNotExist:
        return JsonResponse({'existe': False})
    

def validar_rut_view(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        if Trabajador.objects.filter(rut=rut).exists():
            request.session['rut_validado'] = rut  # ✅ esto es lo importante
            return redirect('registrar_autorizacion')
        else:
            return render(request, 'autorizaciones/validar_rut.html', {
                'error': 'El trabajador no existe.'
            })

    return render(request, 'autorizaciones/validar_rut.html')


def generar_pdf(request, id):
    autorizacion = get_object_or_404(Autorizacion, id=id)

    # Ruta del archivo PDF
    output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs')
    os.makedirs(output_path, exist_ok=True)
    file_name = f"autorizacion_{id}.pdf"
    file_path = os.path.join(output_path, file_name)

    # Crear PDF
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    x = 50
    y = height - 50

    # Cabecera
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, f"Autorización Nº {autorizacion.id}")
    y -= 30

    # Faena desde el nombre del usuario logueado
    faena = ""
    if request.user.username == "bodega_mantos_cobrizos":
        faena = "Mantos Cobrizos"
    elif request.user.username == "bodega_tigresa":
        faena = "Tigresa"
    elif request.user.username == "bodega_revoltosa":
        faena = "Revoltosa"

    c.setFont("Helvetica", 12)
    c.drawString(x, y, f"Faena: {faena}")
    y -= 20
    c.drawString(x, y, f"Trabajador: {autorizacion.nombre_trabajador}")
    y -= 20
    c.drawString(x, y, f"RUT: {autorizacion.rut_trabajador}")
    y -= 20
    c.drawString(x, y, f"Encargado de Bodega: {autorizacion.personal_bodega}")
    y -= 20
    c.drawString(x, y, f"Fecha: {autorizacion.fecha.strftime('%d-%m-%Y %H:%M')}")
    y -= 40

    # EPP solicitados
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "EPP Solicitado:")
    y -= 20
    c.setFont("Helvetica", 11)

    try:
        epp_list = json.loads(autorizacion.epp_solicitado)
    except:
        epp_list = []

    for item in epp_list:
        try:
            epp = EPP.objects.get(id=int(item["id"]))
            c.drawString(x, y, f"{epp.nombre}")
            c.drawString(x + 300, y, f"x{str(item['cantidad'])}")
            y -= 20
        except EPP.DoesNotExist:
            continue

    # Firmas
    y -= 40
    c.drawString(x, y, "Firma Trabajador: ____________________________")
    y -= 30
    c.drawString(x, y, "Firma Encargado de Bodega: ___________________")

    c.save()

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')