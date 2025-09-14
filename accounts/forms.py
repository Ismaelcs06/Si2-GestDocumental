from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Cliente


class BaseClienteForm(forms.ModelForm):
    """Formulario base para datos del usuario que será cliente"""
    
    # Campos del modelo User
    nombres = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese los nombres'
        }),
        label='Nombres'
    )
    
    apellido_paterno = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido paterno'
        }),
        label='Apellido Paterno'
    )
    
    apellido_materno = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido materno (opcional)'
        }),
        label='Apellido Materno'
    )
    
    ci = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1234567-1A'
        }),
        label='Cédula de Identidad'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        }),
        label='Correo Electrónico'
    )
    
    celular = forms.CharField(
        max_length=8,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 71234567'
        }),
        label='Celular'
    )
    
    direccion = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección completa'
        }),
        label='Dirección'
    )
    
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha de Nacimiento'
    )

    class Meta:
        model = User
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'ci', 'email', 
                 'celular', 'direccion', 'fecha_nacimiento']


class ClientePersonaForm(BaseClienteForm):
    """Formulario para registro de cliente persona natural"""
    
    clasificacion_procesal = forms.ChoiceField(
        choices=Cliente.CLASIFICACION,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Clasificación Procesal'
    )
    
    historial = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Historial del cliente (opcional)'
        }),
        label='Historial'
    )
    
    def save(self, commit=True):
        # Crear usuario
        user = User.objects.create_user(
            username=self.cleaned_data['ci'],
            nombres=self.cleaned_data['nombres'],
            apellido_paterno=self.cleaned_data['apellido_paterno'],
            apellido_materno=self.cleaned_data.get('apellido_materno', ''),
            ci=self.cleaned_data['ci'],
            email=self.cleaned_data['email'],
            celular=self.cleaned_data.get('celular', ''),
            direccion=self.cleaned_data.get('direccion', ''),
            fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento')
        )
        
        if commit:
            user.save()
            
            # Crear perfil de cliente
            cliente = Cliente.objects.create(
                user=user,
                tipo_cliente='PERSONA',
                clasificacion_procesal=self.cleaned_data['clasificacion_procesal'],
                historial=self.cleaned_data.get('historial', '')
            )
            return cliente
        
        return user


class ClienteEmpresaForm(BaseClienteForm):
    """Formulario para registro de cliente jurídico (empresa)"""
    
    nombre_empresa = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Razón social de la empresa'
        }),
        label='Nombre de la Empresa'
    )
    
    nit = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1234567890'
        }),
        label='NIT'
    )
    
    clasificacion_procesal = forms.ChoiceField(
        choices=Cliente.CLASIFICACION,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Clasificación Procesal'
    )
    
    historial = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Historial del cliente (opcional)'
        }),
        label='Historial'
    )
    
    def clean_nit(self):
        nit = self.cleaned_data.get('nit')
        if nit and Cliente.objects.filter(nit=nit).exists():
            raise ValidationError('Ya existe un cliente con este NIT.')
        return nit
    
    def save(self, commit=True):
        # Crear usuario (representante legal)
        user = User.objects.create_user(
            username=self.cleaned_data['ci'],
            nombres=self.cleaned_data['nombres'],
            apellido_paterno=self.cleaned_data['apellido_paterno'],
            apellido_materno=self.cleaned_data.get('apellido_materno', ''),
            ci=self.cleaned_data['ci'],
            email=self.cleaned_data['email'],
            celular=self.cleaned_data.get('celular', ''),
            direccion=self.cleaned_data.get('direccion', ''),
            fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento')
        )
        
        if commit:
            user.save()
            
            # Crear perfil de cliente empresa
            cliente = Cliente.objects.create(
                user=user,
                tipo_cliente='EMPRESA',
                nombre_empresa=self.cleaned_data['nombre_empresa'],
                nit=self.cleaned_data['nit'],
                clasificacion_procesal=self.cleaned_data['clasificacion_procesal'],
                historial=self.cleaned_data.get('historial', '')
            )
            return cliente
        
        return user


class ClienteUpdateForm(forms.ModelForm):
    """Formulario para actualizar datos de un cliente existente"""
    
    class Meta:
        model = Cliente
        fields = ['tipo_cliente', 'nombre_empresa', 'nit', 'clasificacion_procesal', 'historial']
        widgets = {
            'tipo_cliente': forms.Select(attrs={'class': 'form-control'}),
            'nombre_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la empresa'
            }),
            'nit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NIT de la empresa'
            }),
            'clasificacion_procesal': forms.Select(attrs={'class': 'form-control'}),
            'historial': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos condicionales según el tipo de cliente
        if self.instance and self.instance.tipo_cliente == 'PERSONA':
            self.fields['nombre_empresa'].widget.attrs['style'] = 'display:none;'
            self.fields['nit'].widget.attrs['style'] = 'display:none;'


class UserUpdateForm(forms.ModelForm):
    """Formulario para actualizar datos del usuario asociado al cliente"""
    
    class Meta:
        model = User
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'email', 
                 'celular', 'direccion', 'fecha_nacimiento']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }