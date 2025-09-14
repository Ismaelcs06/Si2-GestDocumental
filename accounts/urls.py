from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("roles/", views.roles_list, name="roles_list"),
    path("roles/nuevo/", views.role_create, name="role_create"),
    path("roles/<int:pk>/editar/", views.role_edit, name="role_edit"),
    path("roles/<int:pk>/eliminar/", views.role_delete, name="role_delete"),
    path("roles/<int:pk>/permisos/", views.role_permissions, name="role_permissions"),
]
