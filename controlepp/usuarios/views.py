from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Vista login personalizada
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirección según ROL y username específico
            if user.rol == 'admin':
                return redirect('admin_dashboard')
            elif user.rol == 'bodega':
                if user.username == 'bodega_mantos_cobrizos':
                    return redirect('bodega_mantos_cobrizos')
                elif user.username == 'bodega_tigresa':
                    return redirect('bodega_tigresa')
                elif user.username == 'bodega_revoltosa':
                    return redirect('bodega_revoltosa')
                else:
                    return redirect('bodega_dashboard')  # opción general
            elif user.rol == 'prevencion':
                return redirect('prevencion_dashboard')
            else:
                return redirect('login')  # fallback si el rol no está definido
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'usuarios/login.html')
@login_required
def redireccion_por_faena(request):
    usuario = request.user.username.lower()

    if usuario == 'bodega_mantos_blancos':
        return redirect('bodega_mantos_blancos')
    elif usuario == 'bodega_tigresa':
        return redirect('bodega_tigresa')
    elif usuario == 'bodega_revoltosa':
        return redirect('bodega_revoltosa')
    elif usuario == 'prevencion':
        return redirect('prevencion_dashboard')  # si tienes esa vista
    else:
        return redirect('login')  # por defecto

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.rol != 'admin':
        return redirect_to_dashboard(request)
    return render(request, 'dashboards/admin.html')

@login_required
def bodega_dashboard(request):
    if request.user.rol != 'bodega':
        return redirect_to_dashboard(request)
    return render(request, 'dashboards/bodega.html')

