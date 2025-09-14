# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django import forms

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
