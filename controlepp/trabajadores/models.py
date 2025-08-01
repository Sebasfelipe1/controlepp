from django.db import models

class Trabajador(models.Model):
    rut = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    nombre_cargo = models.CharField(max_length=100)


    class Meta:
        db_table = 'trabajador'
        managed = False  # Porque ya existe en la base de datos

    def __str__(self):
        return f"{self.nombre} ({self.rut})"