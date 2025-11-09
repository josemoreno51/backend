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
    list_display = ['diseño', 'flor', 'cantidad', 'subtotal']