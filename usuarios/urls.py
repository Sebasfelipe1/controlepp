from django.urls import path
from . import views
from .views import login_view, logout_view, redireccion_por_faena

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', redireccion_por_faena, name='inicio'),
]