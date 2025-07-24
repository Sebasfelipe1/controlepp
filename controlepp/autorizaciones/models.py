from django.db import models

# Create your models here.


class Autorizacion(models.Model):
    id = models.AutoField(primary_key=True)
    rut_trabajador = models.CharField(max_length=20)
    fecha = models.DateField()
    motivo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'autorizacion'
        managed = False