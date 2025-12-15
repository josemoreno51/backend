"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views  # Importar desde backend
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.shortcuts import redirect

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API de Sistema de Ventas - Floristería",
        default_version='v1',
        description="API RESTful para el sistema de gestión de ventas de floristería",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@floristeria.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Redirección raíz a login
def root_redirect(request):
    return redirect('login')

urlpatterns = [
    # Página principal - Login
    path('', views.custom_login, name='login'),
    
    # Dashboard después del login
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Logout
    path('logout/', views.custom_logout, name='logout'),
    
    # Registro de usuarios
    path('register/', views.register, name='register'),
    
    # Incluir las URLs de ventas
    path('ventas/', include('ventas.urls')),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API REST
    path('api/', include('api.urls')),
    
    # Documentación Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]