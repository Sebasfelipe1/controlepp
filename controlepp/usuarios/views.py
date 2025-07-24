from django.shortcuts import render, redirect

# Create your views here.


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.rol == 'admin':
                return redirect('admin_dashboard')
            elif user.rol == 'bodega':
                return redirect('bodega_dashboard')
            elif user.rol == 'prevencion':
                return redirect('prevencion_dashboard')
            else:
                return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')