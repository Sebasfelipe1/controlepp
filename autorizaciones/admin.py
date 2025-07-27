from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import PerfilUsuario, Autorizacion

admin.site.register(User, UserAdmin)
admin.site.register(PerfilUsuario)
admin.site.register(Autorizacion)

