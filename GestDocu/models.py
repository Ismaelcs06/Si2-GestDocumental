from django.db import models
from django.conf import settings
from .validators import ext_validator, max_size

# ---- Catálogo: Tipo de documento -------------------------------------------
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)


    class Meta:
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipos de documento"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# ---- Núcleo: Caso / Expediente / Documento ---------------------------------
class Caso(models.Model):
    ESTADOS = [
        ("ABIERTO", "Abierto"),
        ("EN_PROCESO", "En proceso"),
        ("CERRADO", "Cerrado"),
        ("ARCHIVADO", "Archivado"),
    ]
    PRIORIDAD = [("BAJA", "Baja"), ("MEDIA", "Media"), ("ALTA", "Alta")]

    nro_caso = models.CharField("Nro. Caso", max_length=50, unique=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default="ABIERTO")
    descripcion = models.TextField(blank=True)
    apelaciones = models.TextField(blank=True)
    tipo_de_caso = models.CharField(max_length=100, blank=True)
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD, default="MEDIA")

    # M2M con perfiles de accounts mediante tablas intermedias
    abogados = models.ManyToManyField("accounts.Abogado", through="Participa", related_name="casos")
    clientes = models.ManyToManyField("accounts.Cliente", through="Tiene", related_name="casos")
    auxiliares = models.ManyToManyField("accounts.Auxiliar", through="Apoya", related_name="casos")

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Caso"
        verbose_name_plural = "Casos"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.nro_caso} — {self.tipo_de_caso or self.descripcion[:30]}"


class Expediente(models.Model):
    ESTADOS = [
        ("ABIERTO", "Abierto"),
        ("CERRADO", "Cerrado"),
        ("ARCHIVADO", "Archivado"),
    ]

    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name="expedientes")
    codigo = models.CharField("Código de expediente", max_length=50)
    fecha_creacion = models.DateField(null=True, blank=True)
    fecha_cierre = models.DateField(null=True, blank=True)
    autoridad = models.CharField(max_length=150, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="ABIERTO")
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"
        unique_together = ("caso", "codigo")
        ordering = ["caso", "codigo"]

    def __str__(self):
        return f"{self.caso.nro_caso} / {self.codigo}"


class Documento(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, related_name="documentos")
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, related_name="documentos")
    nombre = models.CharField(max_length=200)
    
    archivo = models.FileField(
        upload_to="documentos/",
        validators=[ext_validator, max_size]   # 👈 aquí aplicas los validadores
    )
    
    fecha_subida = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="documentos_creados")

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ["-fecha_subida"]

    def __str__(self):
        return self.nombre

# ---- Tablas intermedias con metadatos ---------------------------------------
class Participa(models.Model):  # Caso — Abogado
    ESTADO = [("ACTIVO", "Activo"), ("INACTIVO", "Inactivo")]
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    abogado = models.ForeignKey("accounts.Abogado", on_delete=models.CASCADE)
    rol = models.CharField(max_length=100, blank=True)  # rol procesal del abogado
    estado = models.CharField(max_length=10, choices=ESTADO, default="ACTIVO")
    fecha = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        unique_together = ("caso", "abogado")
        verbose_name = "Participación (Abogado en Caso)"
        verbose_name_plural = "Participaciones (Abogados en Casos)"

    def __str__(self):
        return f"{self.abogado} en {self.caso} — {self.rol or 'Sin rol'}"


class Tiene(models.Model):  # Caso — Cliente
    ESTADO = [("ACTIVO", "Activo"), ("INACTIVO", "Inactivo")]
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    cliente = models.ForeignKey("accounts.Cliente", on_delete=models.CASCADE)
    rol_procesal = models.CharField(max_length=100, blank=True)
    fecha_incorporacion = models.DateField(null=True, blank=True)
    estado_participacion = models.CharField(max_length=10, choices=ESTADO, default="ACTIVO")

    class Meta:
        unique_together = ("caso", "cliente")
        verbose_name = "Vinculación (Cliente en Caso)"
        verbose_name_plural = "Vinculaciones (Clientes en Casos)"

    def __str__(self):
        return f"{self.cliente} en {self.caso}"


class Apoya(models.Model):  # Caso — Auxiliar
    ESTADO = [("ACTIVO", "Activo"), ("FINALIZADO", "Finalizado")]
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    auxiliar = models.ForeignKey("accounts.Auxiliar", on_delete=models.CASCADE)
    tareas = models.CharField(max_length=150, blank=True)
    fecha_ini = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADO, default="ACTIVO")

    class Meta:
        unique_together = ("caso", "auxiliar")
        verbose_name = "Apoyo (Auxiliar en Caso)"
        verbose_name_plural = "Apoyos (Auxiliares en Casos)"

    def __str__(self):
        return f"{self.auxiliar} apoya en {self.caso}"
