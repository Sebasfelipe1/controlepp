from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from autorizaciones.models import Autorizacion
from django.core.paginator import Paginator
from django.conf import settings

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