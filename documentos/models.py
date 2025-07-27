from django.db import models

# Create your models here.


class Documento(models.Model):
    id = models.AutoField(primary_key=True)
    retiro = models.ForeignKey('retiros.RetiroEPP', on_delete=models.DO_NOTHING, db_column='retiro_id')
    archivo_pdf = models.CharField(max_length=255)
    firmado = models.BooleanField(default=False)

    class Meta:
        db_table = 'documento'
        managed = False