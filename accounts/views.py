# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Cliente, User
from .forms import ClientePersonaForm, ClienteEmpresaForm, ClienteUpdateForm, UserUpdateForm

# ---------------------------------------------------------------------
# Configura qué apps del proyecto mostrar en la pantalla de permisos.
# Déjalo en [] o None si quieres ver TODOS los permisos del sistema.
PROJECT_APPS = ["accounts", "gestdocu"]
# ---------------------------------------------------------------------

# =========================
#         FORMS
# =========================
class RoleForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]
        labels = {"name": "Nombre del rol"}


class RolePermissionsForm(forms.Form):
    """Formulario simple para seleccionar múltiples permisos."""
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permisos disponibles",
    )


# =========================
#         VISTAS
# =========================
@login_required
@permission_required("auth.view_group", raise_exception=True)
def roles_list(request):
    """Lista de roles con contadores de permisos y usuarios."""
    roles = Group.objects.all().order_by("name")
    data = [
        {
            "id": r.id,
            "name": r.name,
            "num_perms": r.permissions.count(),
            "num_users": r.user_set.count(),
        }
        for r in roles
    ]
    return render(request, "accounts/roles.html", {"roles": data})


@login_required
@permission_required("auth.add_group", raise_exception=True)
def role_create(request):
    """Crear un nuevo rol."""
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:roles_list")
    else:
        form = RoleForm()
    return render(request, "accounts/roles_form.html", {"form": form, "title": "Nuevo rol"})


@login_required
@permission_required("auth.change_group", raise_exception=True)
def role_edit(request, pk: int):
    """Editar un rol existente."""
    role = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect("accounts:roles_list")
    else:
        form = RoleForm(instance=role)
    return render(request, "accounts/roles_form.html", {"form": form, "title": f"Editar: {role.name}"})


@login_required
@permission_required("auth.delete_group", raise_exception=True)
def role_delete(request, pk: int):
    """Confirmar y eliminar un rol."""
    role = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        role.delete()
        return redirect("accounts:roles_list")
    return render(request, "accounts/role_confirm_delete.html", {"role": role})


@login_required
@permission_required("auth.change_group", raise_exception=True)
def role_permissions(request, pk: int):
    """
    Asignar permisos (auth.Permission) a un rol (Group).
    Muestra los permisos agrupados por app y modelo con checkboxes.
    """
    role = get_object_or_404(Group, pk=pk)

    # Base queryset de permisos
    qs = Permission.objects.select_related("content_type").order_by(
        "content_type__app_label", "content_type__model", "codename"
    )
    # Filtra por apps del proyecto si se configuró
    if PROJECT_APPS:
        qs = qs.filter(content_type__app_label__in=PROJECT_APPS)

    # Instanciamos el form y le inyectamos el queryset filtrado
    form = RolePermissionsForm(request.POST or None)
    form.fields["permissions"].queryset = qs
    form.fields["permissions"].initial = role.permissions.values_list("id", flat=True)

    # Agrupar permisos para el template (app -> modelo -> lista permisos)
    grouped = {}
    for perm in qs:
        app = perm.content_type.app_label
        model = perm.content_type.model
        grouped.setdefault(app, {}).setdefault(model, []).append(perm)

    if request.method == "POST" and form.is_valid():
        role.permissions.set(form.cleaned_data["permissions"])  # reemplaza asignaciones
        return redirect("accounts:roles_list")

    ctx = {
        "role": role,
        "form": form,
        "grouped": grouped,
        "title": f"Permisos de rol: {role.name}",
    }
    return render(request, "accounts/role_permissions.html", ctx)


# =========================
#    VISTAS CRUD CLIENTES
# =========================

@login_required
def clientes_list(request):
    """Lista de clientes con paginación y búsqueda."""
    search = request.GET.get('search', '')
    tipo_filter = request.GET.get('tipo', '')
    clasificacion_filter = request.GET.get('clasificacion', '')
    
    queryset = Cliente.objects.select_related('user').all()
    
    # Filtros de búsqueda
    if search:
        queryset = queryset.filter(
            Q(user__nombres__icontains=search) |
            Q(user__apellido_paterno__icontains=search) |
            Q(user__apellido_materno__icontains=search) |
            Q(user__ci__icontains=search) |
            Q(user__email__icontains=search) |
            Q(nombre_empresa__icontains=search) |
            Q(nit__icontains=search)
        )
    
    if tipo_filter:
        queryset = queryset.filter(tipo_cliente=tipo_filter)
        
    if clasificacion_filter:
        queryset = queryset.filter(clasificacion_procesal=clasificacion_filter)
    
    queryset = queryset.order_by('-user__date_joined')
    
    # Paginación
    paginator = Paginator(queryset, 10)  # 10 clientes por página
    page = request.GET.get('page')
    clientes = paginator.get_page(page)
    
    context = {
        'clientes': clientes,
        'search': search,
        'tipo_filter': tipo_filter,
        'clasificacion_filter': clasificacion_filter,
        'tipos': Cliente.TIPO,
        'clasificaciones': Cliente.CLASIFICACION,
    }
    return render(request, 'accounts/clientes_list.html', context)


@login_required
def cliente_detail(request, pk):
    """Vista detalle de un cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    context = {'cliente': cliente}
    return render(request, 'accounts/cliente_detail.html', context)


@login_required
def cliente_create(request):
    """Vista para crear un nuevo cliente (persona o empresa)."""
    tipo = request.GET.get('tipo', 'PERSONA')
    
    if tipo == 'EMPRESA':
        FormClass = ClienteEmpresaForm
        template_title = 'Registrar Cliente - Empresa'
    else:
        FormClass = ClientePersonaForm
        template_title = 'Registrar Cliente - Persona Natural'
    
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            try:
                cliente = form.save()
                messages.success(request, f'Cliente {cliente.user.nombre_completo} registrado exitosamente.')
                return redirect('accounts:cliente_detail', pk=cliente.pk)
            except Exception as e:
                messages.error(request, f'Error al registrar cliente: {str(e)}')
    else:
        form = FormClass()
    
    context = {
        'form': form,
        'title': template_title,
        'tipo': tipo
    }
    return render(request, 'accounts/cliente_form.html', context)


@login_required
def cliente_update(request, pk):
    """Vista para actualizar un cliente existente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente_form = ClienteUpdateForm(request.POST, instance=cliente)
        user_form = UserUpdateForm(request.POST, instance=cliente.user)
        
        if cliente_form.is_valid() and user_form.is_valid():
            user_form.save()
            cliente_form.save()
            messages.success(request, f'Cliente {cliente.user.nombre_completo} actualizado exitosamente.')
            return redirect('accounts:cliente_detail', pk=cliente.pk)
    else:
        cliente_form = ClienteUpdateForm(instance=cliente)
        user_form = UserUpdateForm(instance=cliente.user)
    
    context = {
        'cliente_form': cliente_form,
        'user_form': user_form,
        'cliente': cliente,
        'title': f'Editar Cliente: {cliente.user.nombre_completo}'
    }
    return render(request, 'accounts/cliente_update.html', context)


@login_required
def cliente_delete(request, pk):
    """Vista para eliminar un cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        nombre = cliente.user.nombre_completo
        # Eliminar usuario también eliminará el cliente por CASCADE
        cliente.user.delete()
        messages.success(request, f'Cliente {nombre} eliminado exitosamente.')
        return redirect('accounts:clientes_list')
    
    context = {
        'cliente': cliente,
        'title': f'Eliminar Cliente: {cliente.user.nombre_completo}'
    }
    return render(request, 'accounts/cliente_confirm_delete.html', context)
