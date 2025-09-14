from django.contrib import admin
from .models import (
    Caso, Expediente, Documento, TipoDocumento,
    Participa, Tiene, Apoya
)

class ParticipaInline(admin.TabularInline):
    model = Participa
    extra = 0

class TieneInline(admin.TabularInline):
    model = Tiene
    extra = 0

class ApoyaInline(admin.TabularInline):
    model = Apoya
    extra = 0

@admin.register(Caso)
class CasoAdmin(admin.ModelAdmin):
    list_display = ("nro_caso", "tipo_de_caso", "estado", "prioridad", "fecha_inicio", "fecha_finalizacion")
    search_fields = ("nro_caso", "tipo_de_caso", "descripcion", "apelaciones")
    list_filter = ("estado", "prioridad")
    inlines = [ParticipaInline, TieneInline, ApoyaInline]

@admin.register(Expediente)
class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ("caso", "codigo", "estado", "fecha_creacion", "fecha_cierre", "autoridad")
    search_fields = ("codigo", "autoridad", "observaciones")
    list_filter = ("estado", "caso")

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "expediente", "creado_por", "fecha_subida")
    search_fields = ("nombre", "observaciones", "expediente__codigo", "expediente__caso__nro_caso")
    list_filter = ("tipo", "fecha_subida")

admin.site.register(TipoDocumento)
