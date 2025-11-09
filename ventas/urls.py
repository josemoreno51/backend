from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # URLs para Clientes
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:id>/', views.cliente_edit, name='cliente_edit'),
    path('clientes/eliminar/<int:id>/', views.cliente_delete, name='cliente_delete'),
    
    # URLs para Categorías
    path('categorias/', views.categorias_list, name='categorias_list'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/editar/<int:id>/', views.categoria_edit, name='categoria_edit'),
    path('categorias/eliminar/<int:id>/', views.categoria_delete, name='categoria_delete'),
    
    # URLs para Productos
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/nuevo/', views.producto_create, name='producto_create'),
    path('productos/editar/<int:id>/', views.producto_edit, name='producto_edit'),
    path('productos/eliminar/<int:id>/', views.producto_delete, name='producto_delete'),
    
    # URLs para Eventos
    path('eventos/', views.eventos_list, name='eventos_list'),
    path('eventos/nuevo/', views.evento_create, name='evento_create'),
    path('eventos/editar/<int:id>/', views.evento_edit, name='evento_edit'),
    path('eventos/eliminar/<int:id>/', views.evento_delete, name='evento_delete'),
    
    # URLs para Ventas
    path('ventas/', views.ventas_list, name='ventas_list'),
    path('ventas/nueva/', views.venta_create, name='venta_create'),
    path('ventas/detalle/<int:id>/', views.venta_detail, name='venta_detail'),
    path('ventas/editar/<int:id>/', views.venta_edit, name='venta_edit'),
    path('ventas/eliminar/<int:id>/', views.venta_delete, name='venta_delete'),
    
    # URLs para Diseño de Ramos (NOMBRES SIMPLIFICADOS)
    path('diseno-ramos/', views.diseno_ramos_list, name='diseno_ramos_list'),
    path('diseno-ramos/nuevo/', views.diseno_ramo_create, name='diseno_ramo_create'),
    path('diseno-ramos/detalle/<int:id>/', views.diseno_ramo_detail, name='diseno_ramo_detail'),
    path('diseno-ramos/convertir/<int:id>/', views.diseno_ramo_convertir_venta, name='diseno_ramo_convertir_venta'),
    path('diseno-ramos/eliminar/<int:id>/', views.diseno_ramo_delete, name='diseno_ramo_delete'),
    
    # URLs para Informes
    path('informes/', views.informes, name='informes'),
]