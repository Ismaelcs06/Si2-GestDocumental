# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django import forms

# ---------------------------------------------------------------------
# Configura qué apps del proyecto mostrar en la pantalla de permisos.
# Déjalo en [] o None si quieres ver TODOS los permisos del sistema.
PROJECT_APPS = ["accounts", "gestdocu"]
# ---------------------------------------------------------------------

User = get_user_model()

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
#      VISTAS: ROLES
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

    qs = Permission.objects.select_related("content_type").order_by(
        "content_type__app_label", "content_type__model", "codename"
    )
    if PROJECT_APPS:
        qs = qs.filter(content_type__app_label__in=PROJECT_APPS)

    form = RolePermissionsForm(request.POST or None)
    form.fields["permissions"].queryset = qs
    form.fields["permissions"].initial = role.permissions.values_list("id", flat=True)

    # Agrupar para el template
    grouped = {}
    for perm in qs:
        app = perm.content_type.app_label
        model = perm.content_type.model
        grouped.setdefault(app, {}).setdefault(model, []).append(perm)

    if request.method == "POST" and form.is_valid():
        role.permissions.set(form.cleaned_data["permissions"])
        messages.success(request, "Permisos actualizados.")
        return redirect("accounts:roles_list")

    ctx = {
        "role": role,
        "form": form,
        "grouped": grouped,
        "title": f"Permisos de rol: {role.name}",
    }
    return render(request, "accounts/role_permissions.html", ctx)


# =========================
#     VISTAS: USUARIOS
# =========================
@login_required
@permission_required("accounts.view_user", raise_exception=True)
def user_list(request):
    """Listado con búsqueda y paginación."""
    q = request.GET.get("q", "").strip()
    users = User.objects.all().order_by("-date_joined")
    if q:
        users = users.filter(username__icontains=q) | users.filter(email__icontains=q)

    paginator = Paginator(users, 10)
    page = request.GET.get("page")
    users_page = paginator.get_page(page)
    return render(request, "accounts/users.html", {"users": users_page, "q": q})


@login_required
@permission_required("accounts.add_user", raise_exception=True)
def user_create(request):
    """Crear usuario y asignar roles (grupos)."""
    from .forms import UserCreateForm
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Usuario '{user.username}' creado.")
            return redirect("accounts:user_list")
    else:
        form = UserCreateForm()
    return render(request, "accounts/user_form.html", {"form": form, "title": "Nuevo usuario"})


@login_required
@permission_required("accounts.change_user", raise_exception=True)
def user_edit(request, pk: int):
    """Editar datos de usuario y sus roles."""
    from .forms import UserUpdateForm
    user = get_object_or_404(User, pk=pk)

    # Evitar que un usuario no-superuser edite superusuarios
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, "No tienes permisos para editar un superusuario.")
        return redirect("accounts:user_list")

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuario '{user.username}' actualizado.")
            return redirect("accounts:user_list")
    else:
        form = UserUpdateForm(instance=user)
    return render(request, "accounts/user_form.html", {"form": form, "title": f"Editar: {user.username}"})


@login_required
@permission_required("accounts.delete_user", raise_exception=True)
def user_delete(request, pk: int):
    """Eliminar usuario (no permite borrar superusuarios)."""
    user = get_object_or_404(User, pk=pk)

    if user.is_superuser:
        messages.error(request, "No puedes eliminar un superusuario.")
        return redirect("accounts:user_list")

    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"Usuario '{username}' eliminado.")
        return redirect("accounts:user_list")
    return render(request, "accounts/user_confirm_delete.html", {"user_obj": user})
