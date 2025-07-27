from django.urls import path
from . import views


urlpatterns = [
    path('bodega/mantos-cobrizos/', views.bodega_mantos_cobrizos_view, name='bodega_mantos_cobrizos'),
    path('bodega/tigresa/', views.bodega_tigresa_view, name='bodega_tigresa'),
    path('bodega/revoltosa/', views.bodega_revoltosa_view, name='bodega_revoltosa'),
]