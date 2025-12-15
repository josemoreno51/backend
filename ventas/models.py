from django.db import models

# PRIMERO: Modelos que no dependen de otros
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    TIPO_CLIENTE = [
        ('minorista', 'Cliente Minorista'),
        ('corporativo', 'Cliente Corporativo'),
        ('eventos', 'Clientes de Eventos'),
    ]
    
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE, default='minorista')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

# SEGUNDO: Modelos que dependen de los anteriores
class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('flores', 'Flores'),
        ('ramos', 'Ramos'),
        ('plantas', 'Plantas'),
        ('accesorios', 'Accesorios'),
        ('arreglos', 'Arreglos Especiales'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO, default='flores')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Evento(models.Model):
    TIPO_EVENTO = [
        ('bodas', 'Bodas'),
        ('cumpleanos', 'Cumpleaños'),
        ('aniversario', 'Aniversario'),
        ('funeral', 'Funeral'),
        ('corporativo', 'Evento Corporativo'),
        ('san_valentin', 'San Valentín'),
        ('dia_madre', 'Día de la Madre'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO, default='bodas')
    fecha_evento = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descripcion = models.TextField()
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_evento_display()}"

# TERCERO: Modelos que dependen de múltiples modelos anteriores
class Venta(models.Model):
    ESTADO_VENTA = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    direccion_entrega = models.TextField(default='Misma dirección del cliente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_VENTA, default='pendiente')
    notas = models.TextField(blank=True)
    
    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    mensaje_tarjeta = models.TextField(blank=True)
    
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"Detalle {self.id} - {self.producto.nombre}"    
from django.db import models

# ... (otros modelos existentes)

class Flor(models.Model):
    COLORES = [
        ('rojo', 'Rojo'),
        ('rosa', 'Rosa'),
        ('blanco', 'Blanco'),
        ('amarillo', 'Amarillo'),
        ('naranja', 'Naranja'),
        ('morado', 'Morado'),
        ('azul', 'Azul'),
        ('multicolor', 'Multicolor'),
    ]
    
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=20, choices=COLORES, default='rojo')
    precio_unidad = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.CharField(max_length=200, blank=True, default='🌹')
    
    def __str__(self):
        return f"{self.nombre} ({self.get_color_display()})"

class DiseñoRamo(models.Model):
    ESTILOS = [
        ('clasico', 'Clásico'),
        ('moderno', 'Moderno'),
        ('rustico', 'Rústico'),
        ('romantico', 'Romántico'),
        ('minimalista', 'Minimalista'),
    ]
    
    nombre = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estilo = models.CharField(max_length=20, choices=ESTILOS, default='clasico')
    precio_base = models.DecimalField(max_digits=8, decimal_places=2, default=15.00)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)
    
    def calcular_total(self):
        total_flores = sum(detalle.subtotal() for detalle in self.detalles.all())
        return self.precio_base + total_flores
    
    def __str__(self):
        return f"Ramo: {self.nombre} - ${self.calcular_total()}"

class DetalleRamo(models.Model):  # CORREGIDO: DetalleRamo (singular)
    diseño = models.ForeignKey(DiseñoRamo, on_delete=models.CASCADE, related_name='detalles')
    #flor = models.ForeignKey(Flor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField(default=1)
    
    def subtotal(self):
        return self.cantidad * self.producto.precio_unidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

# ... (otros modelos existentes)