from django.contrib import admin
from .models import Cliente, Categoria, Producto, Evento, Venta, DetalleVenta, Flor, DiseñoRamo, DetalleRamo

# ... (otros admin registrations)

@admin.register(Flor)
class FlorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color', 'precio_unidad', 'disponible']
    list_filter = ['color', 'disponible']
    search_fields = ['nombre']

class DetalleRamoInline(admin.TabularInline):
    model = DetalleRamo
    extra = 1

@admin.register(DiseñoRamo)
class DiseñoRamoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cliente', 'estilo', 'precio_base', 'fecha_creacion']
    list_filter = ['estilo', 'fecha_creacion']
    inlines = [DetalleRamoInline]
    search_fields = ['nombre', 'cliente__nombre']

@admin.register(DetalleRamo)
class DetalleRamoAdmin(admin.ModelAdmin):
    list_display = ['diseño', 'producto', 'cantidad', 'subtotal']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'tipo', 'precio', 'stock', 'disponible']
    list_filter = ['categoria', 'tipo', 'disponible']
    search_fields = ['nombre', 'descripcion']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'tipo_cliente']
    search_fields = ['nombre', 'email']