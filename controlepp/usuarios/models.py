from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioBodega(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=100)

    class Meta:
        db_table = 'usuario_bodega'
        managed = False

class CustomUser(AbstractUser):
    faena = models.CharField(max_length=50)
    rol = models.CharField(max_length=20)
    