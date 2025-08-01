from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from autorizaciones.models import Autorizacion, EPP
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
import json


@login_required
def redirigir_por_faena(request):
    user = request.user

    if user.username in ['admin', 'prevencion']:
        return redirect('dashboard_general')  # ajusta si es necesario

    try:
        faena = user.perfilusuario.faena
    except:
        return redirect('sin_faena_asignada')

    return redirect('bienvenida_faena', faena=faena.replace("_", "-"))


@login_required
def bienvenida_faena(request, faena):
    faena_slug = faena.replace("-", "_").lower()

    autorizaciones = Autorizacion.objects.filter(faena=faena_slug).order_by('-id')
    paginator = Paginator(autorizaciones, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, f'bodega/{faena_slug}.html', {
        'faena': faena_slug.capitalize(),
        'usuario': request.user.username,
        'page_obj': page_obj,
        'MEDIA_URL': settings.MEDIA_URL
    })

def es_prevencion(user):
    return user.rol == 'prevencion'



@login_required
@user_passes_test(es_prevencion)
def prevencion_dashboard(request):
    autorizaciones = Autorizacion.objects.filter(estado='completada')

    # — Filtros existentes —
    faena = request.GET.get('faena', '').strip()
    if faena:
        autorizaciones = autorizaciones.filter(faena=faena)

    fecha = request.GET.get('fecha', '').strip()
    if fecha:
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            autorizaciones = autorizaciones.filter(fecha__date=fecha_obj)
        except ValueError:
            pass

    # — Nuevo filtro por RUT —
    rut = request.GET.get('rut', '').strip()
    if rut:
        autorizaciones = autorizaciones.filter(rut_trabajador__icontains=rut)

    autorizaciones = autorizaciones.order_by('-fecha')
    paginator = Paginator(autorizaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # — Procesar JSON de epp_solicitado como antes —
    all_ids = set()
    for auth in page_obj:
        try:
            items = json.loads(auth.epp_solicitado)
        except (TypeError, json.JSONDecodeError):
            items = []
        for itm in items:
            all_ids.add(str(itm.get('id')))

    epp_objs = EPP.objects.filter(id__in=all_ids)
    name_map = { str(e.id): e.nombre for e in epp_objs }

    for auth in page_obj:
        try:
            raw = json.loads(auth.epp_solicitado)
        except (TypeError, json.JSONDecodeError):
            raw = []
        auth.items_display = [
            {'nombre': name_map.get(str(item.get('id')), 'Desconocido'),
             'cantidad': item.get('cantidad', 0)}
            for item in raw
        ]

    return render(request, 'dashboards/prevencion.html', {
        'page_obj': page_obj,
        'faena': faena,
        'fecha': fecha,
        'rut': rut,                  # pasamos el nuevo valor al contexto
    })


    #Función de redirección según ROL

    
def redirect_to_dashboard(request):
    messages.warning(request, "No tienes permiso para entrar ahí, fuiste redirigido a tu panel.")
    rol = request.user.rol
    if rol == 'admin':
        return redirect('admin_dashboard')
    elif rol == 'bodega':
        return redirect('bodega_dashboard')
    elif rol == 'prevencion':
        return redirect('prevencion_dashboard')
    return redirect('login')


