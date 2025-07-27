from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def redirigir_por_faena(request):
    user = request.user

    if user.username in ['admin', 'prevencion']:
        return redirect('dashboard_general')  # asegúrate de que esta URL exista

    try:
        faena = user.perfilusuario.faena
    except:
        return redirect('sin_faena_asignada')  # opcional para usuarios sin perfil

    if faena == 'mantos_cobrizos':
        return redirect('bodega_mantos_cobrizos_view')
    elif faena == 'tigresa':
        return redirect('bodega_tigresa_view')
    elif faena == 'revoltosa':
        return redirect('bodega_revoltosa_view')
    else:
        return redirect('sin_faena_asignada')  # fallback
    
@login_required
def bodega_mantos_cobrizos_view(request):
    return render(request, 'bodega/mantos_cobrizos.html')


@login_required
def bodega_tigresa_view(request):
    return render(request, 'bodega/tigresa.html')


@login_required
def bodega_revoltosa_view(request):
    return render(request, 'bodega/revoltosa.html')