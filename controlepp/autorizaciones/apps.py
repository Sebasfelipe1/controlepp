from django.apps import AppConfig


class AutorizacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autorizaciones'


def ready(self):
    import autorizaciones.signals