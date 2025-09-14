from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # URLs para roles
    path("roles/", views.roles_list, name="roles_list"),
    path("roles/nuevo/", views.role_create, name="role_create"),
    path("roles/<int:pk>/editar/", views.role_edit, name="role_edit"),
    path("roles/<int:pk>/eliminar/", views.role_delete, name="role_delete"),
    path("roles/<int:pk>/permisos/", views.role_permissions, name="role_permissions"),
    
    # URLs para clientes
    path("clientes/", views.clientes_list, name="clientes_list"),
    path("clientes/nuevo/", views.cliente_create, name="cliente_create"),
    path("clientes/<int:pk>/", views.cliente_detail, name="cliente_detail"),
    path("clientes/<int:pk>/editar/", views.cliente_update, name="cliente_update"),
    path("clientes/<int:pk>/eliminar/", views.cliente_delete, name="cliente_delete"),
]
