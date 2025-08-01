from django.urls import path, include
from . import views

urlpatterns = [
    path('bodega/<str:faena>/', views.bienvenida_faena, name='bienvenida_faena'),
    path('redirigir/', views.redirigir_por_faena, name='redirigir_por_faena'),
    path('bodega/mantos-cobrizos/', views.bienvenida_faena, {'faena': 'mantos_cobrizos'}, name='bodega_mantos_cobrizos'),
    path('bodega/tigresa/', views.bienvenida_faena, {'faena': 'tigresa'}, name='bodega_tigresa'),
    path('bodega/revoltosa/', views.bienvenida_faena, {'faena': 'revoltosa'}, name='bodega_revoltosa'),
    path('autorizaciones/', include('autorizaciones.urls')),
    path('prevencion/', views.prevencion_dashboard, name='prevencion_dashboard'),
    
    
]