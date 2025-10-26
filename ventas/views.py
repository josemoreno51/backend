from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Producto, Venta, DetalleVenta 
from django.db import models

# Vistas existentes
def home(request):
    total_clientes = Cliente.objects.count()
    total_productos = Producto.objects.count()
    total_ventas = Venta.objects.count()
    
    context = {
        'total_clientes': total_clientes,
        'total_productos': total_productos,
        'total_ventas': total_ventas,
    }
    return render(request, 'ventas/home.html', context)

# CRUD CLIENTES
def clientes_list(request):
    clientes = Cliente.objects.all().order_by('-fecha_registro')
    return render(request, 'ventas/clientes_list.html', {'clientes': clientes})

def cliente_create(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        
        try:
            Cliente.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion
            )
            messages.success(request, 'Cliente creado exitosamente!')
            return redirect('clientes_list')
        except Exception as e:
            messages.error(request, f'Error al crear cliente: {str(e)}')
    
    return render(request, 'ventas/cliente_form.html')

def cliente_edit(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.email = request.POST['email']
        cliente.telefono = request.POST['telefono']
        cliente.direccion = request.POST['direccion']
        
        try:
            cliente.save()
            messages.success(request, 'Cliente actualizado exitosamente!')
            return redirect('clientes_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar cliente: {str(e)}')
    
    return render(request, 'ventas/cliente_form.html', {'cliente': cliente})

def cliente_delete(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, 'Cliente eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar cliente: {str(e)}')
        return redirect('clientes_list')
    
    return render(request, 'ventas/cliente_confirm_delete.html', {'cliente': cliente})

# Vistas para Productos y Ventas (por ahora básicas)
def productos_list(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/productos.html', {'productos': productos})

def ventas_list(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/ventas.html', {'ventas': ventas})
# CRUD PRODUCTOS
def productos_list(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    return render(request, 'ventas/productos_list.html', {'productos': productos})

def producto_create(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        stock = request.POST['stock']
        
        try:
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock
            )
            messages.success(request, 'Producto creado exitosamente!')
            return redirect('productos_list')
        except Exception as e:
            messages.error(request, f'Error al crear producto: {str(e)}')
    
    return render(request, 'ventas/producto_form.html')

def producto_edit(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        
        try:
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente!')
            return redirect('productos_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar producto: {str(e)}')
    
    return render(request, 'ventas/producto_form.html', {'producto': producto})

def producto_delete(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        try:
            producto.delete()
            messages.success(request, 'Producto eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar producto: {str(e)}')
        return redirect('productos_list')
    
    return render(request, 'ventas/producto_confirm_delete.html', {'producto': producto})
# CRUD VENTAS
def ventas_list(request):
    ventas = Venta.objects.all().order_by('-fecha_venta')
    return render(request, 'ventas/ventas_list.html', {'ventas': ventas})

def venta_create(request):
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        detalles_data = request.POST.getlist('detalles[]')
        
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            venta = Venta.objects.create(cliente=cliente)
            
            # Procesar detalles de venta
            total_venta = 0
            for i in range(0, len(detalles_data), 3):
                if i + 2 < len(detalles_data):
                    producto_id = detalles_data[i]
                    cantidad = detalles_data[i + 1]
                    precio_unitario = detalles_data[i + 2]
                    
                    if producto_id and cantidad and precio_unitario:
                        producto = Producto.objects.get(id=producto_id)
                        detalle = DetalleVenta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=int(cantidad),
                            precio_unitario=float(precio_unitario)
                        )
                        total_venta += detalle.subtotal()
            
            venta.total = total_venta
            venta.save()
            
            messages.success(request, 'Venta creada exitosamente!')
            return redirect('ventas_list')
        except Exception as e:
            messages.error(request, f'Error al crear venta: {str(e)}')
    
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    return render(request, 'ventas/venta_form.html', {
        'clientes': clientes,
        'productos': productos
    })

def venta_detail(request, id):
    venta = get_object_or_404(Venta, id=id)
    detalles = venta.detalleventa_set.all()
    return render(request, 'ventas/venta_detail.html', {
        'venta': venta,
        'detalles': detalles
    })

def venta_delete(request, id):
    venta = get_object_or_404(Venta, id=id)
    
    if request.method == 'POST':
        try:
            venta.delete()
            messages.success(request, 'Venta eliminada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar venta: {str(e)}')
        return redirect('ventas_list')
    
    return render(request, 'ventas/venta_confirm_delete.html', {'venta': venta})
# INFORMES Y GRÁFICOS
def informes(request):
    # Productos más vendidos
    productos_mas_vendidos = DetalleVenta.objects.values(
        'producto__nombre'
    ).annotate(
        total_vendido=models.Sum('cantidad')
    ).order_by('-total_vendido')[:10]

    # Clientes con más ventas
    clientes_con_mas_ventas = Venta.objects.values(
        'cliente__nombre'
    ).annotate(
        total_ventas=models.Count('id'),
        monto_total=models.Sum('total')
    ).order_by('-monto_total')[:10]

    # Preparar datos para gráficos
    productos_labels = [p['producto__nombre'] for p in productos_mas_vendidos]
    productos_data = [p['total_vendido'] for p in productos_mas_vendidos]

    clientes_labels = [c['cliente__nombre'] for c in clientes_con_mas_ventas]
    clientes_data = [float(c['monto_total']) for c in clientes_con_mas_ventas]

    context = {
        'productos_mas_vendidos': productos_mas_vendidos,
        'clientes_con_mas_ventas': clientes_con_mas_ventas,
        'productos_labels': productos_labels,
        'productos_data': productos_data,
        'clientes_labels': clientes_labels,
        'clientes_data': clientes_data,
    }
    return render(request, 'ventas/informes.html', context)