from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioBodega(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=100)

    class Meta:
        db_table = 'usuario_bodega'


class CustomUser(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('bodega', 'Bodega'),
        ('prevencion', 'Prevención'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='bodega')