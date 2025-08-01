from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_autorizacion, name='registrar_autorizacion'),
    path('lista/', views.lista_autorizaciones, name='lista_autorizaciones'),
    path('epp/agregar/', views.agregar_epp, name='agregar_epp'),
    path('vista-previa/<int:id>/', views.vista_previa_autorizacion, name='vista_previa_autorizacion'),
    path('epp/', views.lista_epp, name='lista_epp'),
    path('epp/agregar/', views.agregar_epp, name='agregar_epp'),
    path('epp/editar/<int:id>/', views.editar_epp, name='editar_epp'),
    path('epp/eliminar/<int:id>/', views.eliminar_epp, name='eliminar_epp'),
    path('verificar-trabajador/', views.verificar_trabajador, name='verificar_trabajador'),
    path('validar_rut/', views.validar_rut_view, name='validar_rut'),
    path('pdf/<int:id>/', views.generar_pdf, name='generar_pdf'),
    path('<int:autorizacion_id>/subir-firmado/', views.subir_documento_firmado, name='subir_documento_firmado'),
    path('prevencion/autorizaciones/', views.lista_autorizaciones_prevencion, name='lista_autorizaciones_prevencion'),


]