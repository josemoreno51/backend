from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # URLs para Clientes (CRUD)
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:id>/', views.cliente_edit, name='cliente_edit'),
    path('clientes/eliminar/<int:id>/', views.cliente_delete, name='cliente_delete'),
    
    # URLs para Productos (CRUD)
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/nuevo/', views.producto_create, name='producto_create'),
    path('productos/editar/<int:id>/', views.producto_edit, name='producto_edit'),
    path('productos/eliminar/<int:id>/', views.producto_delete, name='producto_delete'),
    
    # URLs para Ventas (CRUD)
    path('ventas/', views.ventas_list, name='ventas_list'),
    path('ventas/nueva/', views.venta_create, name='venta_create'),
    path('ventas/detalle/<int:id>/', views.venta_detail, name='venta_detail'),
    path('ventas/eliminar/<int:id>/', views.venta_delete, name='venta_delete'),
        # URLs para Informes
    path('informes/', views.informes, name='informes'),
] 