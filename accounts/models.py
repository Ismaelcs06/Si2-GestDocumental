from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


# Validadores
solo_letras = RegexValidator(
    regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
    message="Este campo solo puede contener letras y espacios."
)

celular_bo = RegexValidator(
    regex=r'^[67]\d{7}$',
    message="El celular debe comenzar con 6 o 7 y tener exactamente 8 dígitos."
)

ci_boliviano = RegexValidator(
    regex=r'^\d{5,8}(-[A-Z0-9]{1,3})?$',
    message="El CI debe tener entre 5-8 dígitos, opcionalmente seguido de guion y extensión (ej: 1234567-1A)."
)

nit_boliviano = RegexValidator(
    regex=r'^\d{7,15}$',
    message="El NIT debe contener entre 7 y 15 dígitos."
)

class User(AbstractUser):
    # === Datos personales (del diagrama) ===
    nombres           = models.CharField("Nombres", max_length=50, validators=[solo_letras])
    apellido_paterno  = models.CharField("Apellido paterno", max_length=30, validators=[solo_letras])
    apellido_materno  = models.CharField("Apellido materno", max_length=30, blank=True, validators=[solo_letras])
    direccion         = models.CharField("Dirección", max_length=200, blank=True)  # ← agregado por tu diagrama
    fecha_nacimiento  = models.DateField("Fecha de nacimiento", null=True, blank=True)
    email             = models.EmailField("Email", unique=True)
    ci                = models.CharField("CI", max_length=20, unique=True, validators=[ci_boliviano])
    celular           = models.CharField("Celular", max_length=8, blank=True, validators=[celular_bo])

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        indexes = [
            models.Index(fields=["ci"]),
            models.Index(fields=["email"]),
            models.Index(fields=["apellido_paterno", "apellido_materno", "nombres"]),
        ]

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}".strip()

    def __str__(self):
        return self.nombre_completo or self.username


# === Especializaciones (generalización 1–1 con Usuario) ===

class Abogado(models.Model):
    ESTADO_LICENCIA = [
        ("VIGENTE", "Vigente"),
        ("SUSPENDIDA", "Suspendida"),
        ("VENCIDA", "Vencida"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="abogado")
    nro_credencial = models.CharField("Nro. credencial", max_length=50, unique=True)
    estado_licencia = models.CharField("Estado licencia", max_length=10, choices=ESTADO_LICENCIA, default="VIGENTE")
    especialidad = models.CharField("Especialidad", max_length=100, blank=True, validators=[solo_letras])
    fecha_ingreso = models.DateField("Fecha de ingreso", null=True, blank=True)

    class Meta:
        verbose_name = "Abogado"
        verbose_name_plural = "Abogados"

    def __str__(self):
        return f"Abogado: {self.user.nombre_completo}"


class Cliente(models.Model):
    TIPO = [("PERSONA", "Persona"), ("EMPRESA", "Empresa")]
    CLASIFICACION = [
        ("DEMANDANTE", "Demandante"),
        ("DEMANDADO", "Demandado"),
        ("OTRO", "Otro")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente")
    tipo_cliente = models.CharField("Tipo de cliente", max_length=10, choices=TIPO, default="PERSONA")
    nombre_empresa = models.CharField("Nombre empresa", max_length=150, blank=True)
    nit = models.CharField("NIT", max_length=15, blank=True, validators=[nit_boliviano])
    clasificacion_procesal = models.CharField("Clasificación procesal", max_length=15, choices=CLASIFICACION, default="OTRO")
    historial = models.TextField("Historial", blank=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def clean(self):
        """Validaciones personalizadas del modelo"""
        from django.core.exceptions import ValidationError
        errors = {}
        
        # Validar que empresas tengan NIT
        if self.tipo_cliente == 'EMPRESA' and not self.nit:
            errors['nit'] = 'Las empresas deben tener un NIT registrado.'
            
        # Validar que empresas tengan nombre de empresa
        if self.tipo_cliente == 'EMPRESA' and not self.nombre_empresa:
            errors['nombre_empresa'] = 'Las empresas deben tener un nombre registrado.'
            
        # Validar que personas no tengan NIT ni nombre de empresa
        if self.tipo_cliente == 'PERSONA':
            if self.nit:
                errors['nit'] = 'Las personas naturales no deben tener NIT.'
            if self.nombre_empresa:
                errors['nombre_empresa'] = 'Las personas naturales no deben tener nombre de empresa.'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cliente: {self.user.nombre_completo}"


class Auxiliar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="auxiliar")
    especialidad = models.CharField("Especialidad", max_length=100, blank=True, validators=[solo_letras])
    horario = models.CharField("Horario", max_length=100, blank=True)
    supervisor = models.ForeignKey(Abogado, on_delete=models.SET_NULL, null=True, blank=True, related_name="auxiliares")

    class Meta:
        verbose_name = "Auxiliar"
        verbose_name_plural = "Auxiliares"

    def __str__(self):
        return f"Auxiliar: {self.user.nombre_completo}"
