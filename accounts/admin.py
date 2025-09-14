from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from .models import User, Abogado, Cliente, Auxiliar

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "nombres", "apellido_paterno", "apellido_materno",
                    "email", "ci", "celular", "is_staff", "is_active")
    search_fields = ("nombres", "apellido_paterno", "apellido_materno", "email", "ci", "username")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Datos personales", {"fields": ("nombres", "apellido_paterno", "apellido_materno",
                                         "direccion", "fecha_nacimiento", "email", "ci", "celular")}),
        ("Roles y permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2",
                       "nombres", "apellido_paterno", "apellido_materno",
                       "direccion", "fecha_nacimiento", "email", "ci", "celular",
                       "is_active", "is_staff", "is_superuser", "groups"),
        }),
    )

# Registros simples para ver perfiles en admin
@admin.register(Abogado)
class AbogadoAdmin(admin.ModelAdmin):
    list_display = ("user", "nro_credencial", "estado_licencia", "especialidad", "fecha_ingreso")
    search_fields = ("user__nombres", "user__apellido_paterno", "nro_credencial", "especialidad")
    list_filter = ("estado_licencia",)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("user", "tipo_cliente", "nombre_empresa")
    search_fields = ("user__nombres", "user__apellido_paterno", "nombre_empresa")
    list_filter = ("tipo_cliente",)

@admin.register(Auxiliar)
class AuxiliarAdmin(admin.ModelAdmin):
    list_display = ("user", "especialidad", "horario", "supervisor")
    search_fields = ("user__nombres", "user__apellido_paterno", "especialidad")
