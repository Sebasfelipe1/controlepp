from django.shortcuts import render, redirect
from .models import Autorizacion
from trabajadores.models import Trabajador  # ✅ ESTA LÍNEA

def lista_autorizaciones(request):
    autorizaciones = Autorizacion.objects.all().order_by('-fecha')

    for a in autorizaciones:
        try:
            trabajador = Trabajador.objects.get(rut=a.rut_trabajador)
            a.nombre_trabajador = trabajador.nombre
        except Trabajador.DoesNotExist:
            a.nombre_trabajador = "Desconocido"

    return render(request, 'autorizaciones/lista.html', {'autorizaciones': autorizaciones})