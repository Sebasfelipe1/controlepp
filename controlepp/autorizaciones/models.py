from django.db import models
from django.conf import settings

##USUARIO POR FAENA"
FAENAS = [
    ('mantos_cobrizos', 'Mantos cobrizos'),
    ('tigresa', 'Tigresa'),
    ('revoltosa', 'Revoltosa'),
]

class PerfilUsuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    faena = models.CharField(max_length=20, choices=FAENAS, null=True, blank=True)


class Autorizacion(models.Model):
    rut_trabajador = models.CharField(max_length=20)
    nombre_trabajador = models.CharField(max_length=100)
    epp_solicitado = models.TextField()
    personal_bodega = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    pdf_generado = models.BooleanField(default=False)
    faena = models.CharField(max_length=20, choices=FAENAS, default='mantos_blancos')
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('completada', 'Completada')],
        default='pendiente'
    )
    pdf_generado = models.FileField(
        upload_to='autorizaciones_pdf/pendientes/',
        null=True,
        blank=True
    )
    documento_firmado = models.FileField(
        upload_to='autorizaciones_pdf/completadas/',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'autorizacion'

    def __str__(self):
        return f"{self.nombre_trabajador} ({self.rut_trabajador}) - {self.fecha.strftime('%d-%m-%Y')}"
    

class EPP(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'epp'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    

    def __str__(self):
        return f"{self.user.username} - {self.get_faena_display()}"


