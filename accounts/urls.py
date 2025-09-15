from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "accounts"

urlpatterns = [
    path("roles/", views.roles_list, name="roles_list"),
    path("roles/nuevo/", views.role_create, name="role_create"),
    path("roles/<int:pk>/editar/", views.role_edit, name="role_edit"),
    path("roles/<int:pk>/eliminar/", views.role_delete, name="role_delete"),
    path("roles/<int:pk>/permisos/", views.role_permissions, name="role_permissions"),
    

    # Usuarios
    path("usuarios/", views.user_list, name="user_list"),
    path("usuarios/nuevo/", views.user_create, name="user_create"),
    path("usuarios/<int:pk>/editar/", views.user_edit, name="user_edit"),
    path("usuarios/<int:pk>/eliminar/", views.user_delete, name="user_delete"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
