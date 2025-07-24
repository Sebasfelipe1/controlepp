from django.db import models

# Create your models here.

class RetiroEPP(models.Model):
    id = models.AutoField(primary_key=True)
    autorizacion = models.ForeignKey('autorizaciones.Autorizacion', on_delete=models.DO_NOTHING, db_column='autorizacion_id')
    rut_trabajador = models.CharField(max_length=20)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=20)  # 'Pendiente' o 'Aprobado'
    correlativo = models.CharField(max_length=50, blank=True, null=True)
    usuario_bodega = models.ForeignKey('usuarios.UsuarioBodega', on_delete=models.DO_NOTHING, db_column='usuario_bodega_id')

    class Meta:
        db_table = 'retiro_epp'
        managed = False

class ElementoRetirado(models.Model):
    id = models.AutoField(primary_key=True)
    retiro = models.ForeignKey('retiros.RetiroEPP', on_delete=models.DO_NOTHING, db_column='retiro_id')
    nombre_elemento = models.CharField(max_length=100)

    class Meta:
        db_table = 'elemento_retirado'
        managed = False