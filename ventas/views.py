from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from django.contrib.auth.decorators import login_required  # ✅ AGREGAR ESTA LÍNEA
from .models import Cliente, Categoria, Producto, Evento, Venta, DetalleVenta, Flor, DiseñoRamo, DetalleRamo

# ✅ AGREGAR @login_required A TODAS LAS FUNCIONES

@login_required
def home(request):
    # Estadísticas para el dashboard de floristería
    total_clientes = Cliente.objects.count()
    total_productos = Producto.objects.count()
    total_ventas = Venta.objects.count()
    total_eventos = Evento.objects.count()
    ventas_pendientes = Venta.objects.filter(estado='pendiente').count()
    
    # Productos por categoría para el dashboard
    productos_por_categoria = Producto.objects.values(
        'categoria__nombre'
    ).annotate(
        total=models.Count('id')
    )
    
    context = {
        'total_clientes': total_clientes,
        'total_productos': total_productos,
        'total_ventas': total_ventas,
        'total_eventos': total_eventos,
        'ventas_pendientes': ventas_pendientes,
        'productos_por_categoria': productos_por_categoria,
    }
    return render(request, 'ventas/home.html', context)

# ========== CRUD CLIENTES ==========
@login_required
def clientes_list(request):
    tipo_filtro = request.GET.get('tipo', '')
    clientes = Cliente.objects.all().order_by('-fecha_registro')
    
    if tipo_filtro:
        clientes = clientes.filter(tipo_cliente=tipo_filtro)
    
    return render(request, 'ventas/clientes_list.html', {
        'clientes': clientes,
        'tipo_filtro': tipo_filtro
    })

@login_required
def cliente_create(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        tipo_cliente = request.POST['tipo_cliente']
        
        try:
            Cliente.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                tipo_cliente=tipo_cliente
            )
            messages.success(request, 'Cliente creado exitosamente!')
            return redirect('clientes_list')
        except Exception as e:
            messages.error(request, f'Error al crear cliente: {str(e)}')
    
    return render(request, 'ventas/cliente_form.html')

@login_required
def cliente_edit(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.email = request.POST['email']
        cliente.telefono = request.POST['telefono']
        cliente.direccion = request.POST['direccion']
        cliente.tipo_cliente = request.POST['tipo_cliente']
        
        try:
            cliente.save()
            messages.success(request, 'Cliente actualizado exitosamente!')
            return redirect('clientes_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar cliente: {str(e)}')
    
    return render(request, 'ventas/cliente_form.html', {'cliente': cliente})

@login_required
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

# ========== CRUD CATEGORÍAS ==========
@login_required
def categorias_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'ventas/categorias_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        
        try:
            Categoria.objects.create(
                nombre=nombre,
                descripcion=descripcion
            )
            messages.success(request, 'Categoría creada exitosamente!')
            return redirect('categorias_list')
        except Exception as e:
            messages.error(request, f'Error al crear categoría: {str(e)}')
    
    return render(request, 'ventas/categoria_form.html')

@login_required
def categoria_edit(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        categoria.nombre = request.POST['nombre']
        categoria.descripcion = request.POST['descripcion']
        
        try:
            categoria.save()
            messages.success(request, 'Categoría actualizada exitosamente!')
            return redirect('categorias_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar categoría: {str(e)}')
    
    return render(request, 'ventas/categoria_form.html', {'categoria': categoria})

@login_required
def categoria_delete(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, 'Categoría eliminada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar categoría: {str(e)}')
        return redirect('categorias_list')
    
    return render(request, 'ventas/categoria_confirm_delete.html', {'categoria': categoria})

# ========== CRUD PRODUCTOS ==========
@login_required
def productos_list(request):
    categoria_filtro = request.GET.get('categoria', '')
    tipo_filtro = request.GET.get('tipo', '')
    
    productos = Producto.objects.all().order_by('-fecha_creacion')
    
    if categoria_filtro:
        productos = productos.filter(categoria_id=categoria_filtro)
    if tipo_filtro:
        productos = productos.filter(tipo=tipo_filtro)
    
    categorias = Categoria.objects.all()
    
    return render(request, 'ventas/productos_list.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_filtro': categoria_filtro,
        'tipo_filtro': tipo_filtro
    })

@login_required
def producto_create(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        categoria_id = request.POST['categoria']
        tipo = request.POST['tipo']
        precio = request.POST['precio']
        stock = request.POST['stock']
        disponible = 'disponible' in request.POST
        
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                categoria=categoria,
                tipo=tipo,
                precio=precio,
                stock=stock,
                disponible=disponible
            )
            messages.success(request, 'Producto creado exitosamente!')
            return redirect('productos_list')
        except Exception as e:
            messages.error(request, f'Error al crear producto: {str(e)}')
    
    categorias = Categoria.objects.all()
    return render(request, 'ventas/producto_form.html', {'categorias': categorias})

@login_required
def producto_edit(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.categoria_id = request.POST['categoria']
        producto.tipo = request.POST['tipo']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.disponible = 'disponible' in request.POST
        
        try:
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente!')
            return redirect('productos_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar producto: {str(e)}')
    
    categorias = Categoria.objects.all()
    return render(request, 'ventas/producto_form.html', {
        'producto': producto,
        'categorias': categorias
    })

@login_required
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

# ========== CRUD EVENTOS ==========
@login_required
def eventos_list(request):
    tipo_filtro = request.GET.get('tipo', '')
    
    eventos = Evento.objects.all().order_by('fecha_evento')
    
    if tipo_filtro:
        eventos = eventos.filter(tipo_evento=tipo_filtro)
    
    return render(request, 'ventas/eventos_list.html', {
        'eventos': eventos,
        'tipo_filtro': tipo_filtro
    })

@login_required
def evento_create(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        tipo_evento = request.POST['tipo_evento']
        fecha_evento = request.POST['fecha_evento']
        cliente_id = request.POST['cliente']
        descripcion = request.POST['descripcion']
        
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            Evento.objects.create(
                nombre=nombre,
                tipo_evento=tipo_evento,
                fecha_evento=fecha_evento,
                cliente=cliente,
                descripcion=descripcion
            )
            messages.success(request, 'Evento creado exitosamente!')
            return redirect('eventos_list')
        except Exception as e:
            messages.error(request, f'Error al crear evento: {str(e)}')
    
    clientes = Cliente.objects.all()
    return render(request, 'ventas/evento_form.html', {'clientes': clientes})

@login_required
def evento_edit(request, id):
    evento = get_object_or_404(Evento, id=id)
    
    if request.method == 'POST':
        evento.nombre = request.POST['nombre']
        evento.tipo_evento = request.POST['tipo_evento']
        evento.fecha_evento = request.POST['fecha_evento']
        evento.cliente_id = request.POST['cliente']
        evento.descripcion = request.POST['descripcion']
        
        try:
            evento.save()
            messages.success(request, 'Evento actualizado exitosamente!')
            return redirect('eventos_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar evento: {str(e)}')
    
    clientes = Cliente.objects.all()
    return render(request, 'ventas/evento_form.html', {
        'evento': evento,
        'clientes': clientes
    })

@login_required
def evento_delete(request, id):
    evento = get_object_or_404(Evento, id=id)
    
    if request.method == 'POST':
        try:
            evento.delete()
            messages.success(request, 'Evento eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar evento: {str(e)}')
        return redirect('eventos_list')
    
    return render(request, 'ventas/evento_confirm_delete.html', {'evento': evento})

# ========== CRUD VENTAS ==========
@login_required
def ventas_list(request):
    estado_filtro = request.GET.get('estado', '')
    
    ventas = Venta.objects.all().order_by('-fecha_venta')
    
    if estado_filtro:
        ventas = ventas.filter(estado=estado_filtro)
    
    return render(request, 'ventas/ventas_list.html', {
        'ventas': ventas,
        'estado_filtro': estado_filtro
    })

@login_required
def venta_create(request):
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        evento_id = request.POST.get('evento', '')
        fecha_entrega = request.POST['fecha_entrega']
        direccion_entrega = request.POST['direccion_entrega']
        estado = request.POST['estado']
        notas = request.POST['notas']
        detalles_data = request.POST.getlist('detalles[]')
        mensajes_data = request.POST.getlist('mensajes[]')
        
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            evento = Evento.objects.get(id=evento_id) if evento_id else None
            
            venta = Venta.objects.create(
                cliente=cliente,
                evento=evento,
                fecha_entrega=fecha_entrega,
                direccion_entrega=direccion_entrega,
                estado=estado,
                notas=notas
            )
            
            # Procesar detalles de venta
            total_venta = 0
            for i in range(0, len(detalles_data), 3):
                if i + 2 < len(detalles_data):
                    producto_id = detalles_data[i]
                    cantidad = detalles_data[i + 1]
                    precio_unitario = detalles_data[i + 2]
                    mensaje_tarjeta = mensajes_data[i // 3] if i // 3 < len(mensajes_data) else ''
                    
                    if producto_id and cantidad and precio_unitario:
                        producto = Producto.objects.get(id=producto_id)
                        detalle = DetalleVenta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=int(cantidad),
                            precio_unitario=float(precio_unitario),
                            mensaje_tarjeta=mensaje_tarjeta
                        )
                        total_venta += detalle.subtotal()
            
            venta.total = total_venta
            venta.save()
            
            messages.success(request, 'Venta creada exitosamente!')
            return redirect('ventas_list')
        except Exception as e:
            messages.error(request, f'Error al crear venta: {str(e)}')
    
    clientes = Cliente.objects.all()
    eventos = Evento.objects.all()
    productos = Producto.objects.filter(disponible=True)
    
    return render(request, 'ventas/venta_form.html', {
        'clientes': clientes,
        'eventos': eventos,
        'productos': productos
    })

@login_required
def venta_detail(request, id):
    venta = get_object_or_404(Venta, id=id)
    detalles = venta.detalleventa_set.all()
    return render(request, 'ventas/venta_detail.html', {
        'venta': venta,
        'detalles': detalles
    })

@login_required
def venta_edit(request, id):
    venta = get_object_or_404(Venta, id=id)
    
    if request.method == 'POST':
        venta.cliente_id = request.POST['cliente']
        venta.evento_id = request.POST.get('evento', '') or None
        venta.fecha_entrega = request.POST['fecha_entrega']
        venta.direccion_entrega = request.POST['direccion_entrega']
        venta.estado = request.POST['estado']
        venta.notas = request.POST['notas']
        
        try:
            venta.save()
            messages.success(request, 'Venta actualizada exitosamente!')
            return redirect('ventas_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar venta: {str(e)}')
    
    clientes = Cliente.objects.all()
    eventos = Evento.objects.all()
    return render(request, 'ventas/venta_edit.html', {
        'venta': venta,
        'clientes': clientes,
        'eventos': eventos
    })

@login_required
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

# ========== INFORMES FLORISTERÍA ==========
@login_required
def informes(request):
    # Productos más vendidos (flores más populares)
    productos_mas_vendidos = DetalleVenta.objects.values(
        'producto__nombre', 'producto__tipo', 'producto__categoria__nombre'
    ).annotate(
        total_vendido=models.Sum('cantidad'),
        monto_total=models.Sum(models.F('cantidad') * models.F('precio_unitario'))
    ).order_by('-total_vendido')[:10]

    # Clientes con más compras
    clientes_con_mas_compras = Venta.objects.values(
        'cliente__nombre', 'cliente__tipo_cliente'
    ).annotate(
        total_ventas=models.Count('id'),
        monto_total=models.Sum('total')
    ).order_by('-monto_total')[:10]

    # Eventos más populares
    eventos_populares = Evento.objects.values(
        'tipo_evento'
    ).annotate(
        total_eventos=models.Count('id')
    ).order_by('-total_eventos')

    # Ventas por estado
    ventas_por_estado = Venta.objects.values(
        'estado'
    ).annotate(
        total=models.Count('id')
    )

    # Preparar datos para gráficos
    productos_labels = [f"{p['producto__nombre']} ({p['producto__tipo']})" for p in productos_mas_vendidos]
    productos_data = [p['total_vendido'] for p in productos_mas_vendidos]

    clientes_labels = [c['cliente__nombre'] for c in clientes_con_mas_compras]
    clientes_data = [float(c['monto_total']) for c in clientes_con_mas_compras]

    eventos_labels = [e['tipo_evento'] for e in eventos_populares]
    eventos_data = [e['total_eventos'] for e in eventos_populares]

    context = {
        'productos_mas_vendidos': productos_mas_vendidos,
        'clientes_con_mas_compras': clientes_con_mas_compras,
        'eventos_populares': eventos_populares,
        'ventas_por_estado': ventas_por_estado,
        'productos_labels': productos_labels,
        'productos_data': productos_data,
        'clientes_labels': clientes_labels,
        'clientes_data': clientes_data,
        'eventos_labels': eventos_labels,
        'eventos_data': eventos_data,
    }
    return render(request, 'ventas/informes.html', context)

# ========== SISTEMA DE DISEÑO DE RAMOS ==========
@login_required
def diseno_ramos_list(request):
    diseños = DiseñoRamo.objects.all().order_by('-fecha_creacion')
    return render(request, 'ventas/diseno_ramos_list.html', {'diseños': diseños})

@login_required
def diseno_ramo_create(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        cliente_id = request.POST['cliente']
        estilo = request.POST['estilo']
        precio_base = request.POST.get('precio_base', 15.00)
        notas = request.POST['notas']
        
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            diseño = DiseñoRamo.objects.create(
                nombre=nombre,
                cliente=cliente,
                estilo=estilo,
                precio_base=precio_base,
                notas=notas
            )
            
            # Procesar flores seleccionadas
            flores_data = request.POST.getlist('flores[]')
            cantidades_data = request.POST.getlist('cantidades[]')
            
            for i in range(len(flores_data)):
                if flores_data[i] and cantidades_data[i]:
                    flor = Flor.objects.get(id=flores_data[i])
                    DetalleRamo.objects.create(
                        diseño=diseño,
                        flor=flor,
                        cantidad=int(cantidades_data[i])
                    )
            
            messages.success(request, '¡Diseño de ramo creado exitosamente!')
            return redirect('diseno_ramos_list')
        except Exception as e:
            messages.error(request, f'Error al crear diseño: {str(e)}')
    
    clientes = Cliente.objects.all()
    flores = Flor.objects.filter(disponible=True)
    return render(request, 'ventas/diseno_ramo_form.html', {
        'clientes': clientes,
        'flores': flores
    })

@login_required
def diseno_ramo_detail(request, id):
    diseño = get_object_or_404(DiseñoRamo, id=id)
    detalles = diseño.detalles.all()
    total = diseño.calcular_total()
    
    return render(request, 'ventas/diseno_ramo_detail.html', {
        'diseño': diseño,
        'detalles': detalles,
        'total': total
    })

@login_required
def diseno_ramo_convertir_venta(request, id):
    diseño = get_object_or_404(DiseñoRamo, id=id)
    
    if request.method == 'POST':
        try:
            # Crear venta a partir del diseño
            venta = Venta.objects.create(
                cliente=diseño.cliente,
                total=diseño.calcular_total(),
                estado='pendiente',
                notas=f"Venta generada desde diseño: {diseño.nombre}\n{diseño.notas}"
            )
            
            # Crear detalles de venta
            for detalle_ramo in diseño.detalles.all():
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=Producto.objects.filter(nombre__icontains=detalle_ramo.flor.nombre).first() or Producto.objects.first(),
                    cantidad=detalle_ramo.cantidad,
                    precio_unitario=detalle_ramo.flor.precio_unidad
                )
            
            messages.success(request, '¡Diseño convertido a venta exitosamente!')
            return redirect('ventas_list')
        except Exception as e:
            messages.error(request, f'Error al convertir diseño: {str(e)}')
    
    return redirect('diseno_ramo_detail', id=id)

@login_required
def diseno_ramo_delete(request, id):
    diseño = get_object_or_404(DiseñoRamo, id=id)
    
    if request.method == 'POST':
        try:
            diseño.delete()
            messages.success(request, 'Diseño eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar diseño: {str(e)}')
        return redirect('diseno_ramos_list')
    
    return render(request, 'ventas/diseno_ramo_confirm_delete.html', {'diseño': diseño})