# backend/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ventas.models import Cliente, Producto, Venta, Evento
from django.db import models
from .forms import CustomUserCreationForm

def custom_login(request):
    """Página de login - primera página que ven los usuarios"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido/a {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')  # ✅ Ahora en backend/templates/

@login_required
def dashboard(request):
    """Dashboard principal después del login"""
    # Estadísticas para el dashboard
    total_clientes = Cliente.objects.count()
    total_productos = Producto.objects.count()
    total_ventas = Venta.objects.count()
    total_eventos = Evento.objects.count()
    
    context = {
        'total_clientes': total_clientes,
        'total_productos': total_productos,
        'total_ventas': total_ventas,
        'total_eventos': total_eventos,
    }
    return render(request, 'dashboard.html', context)  # ✅ Ahora en backend/templates/

def custom_logout(request):
    """Cerrar sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente')
    return redirect('login')
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')  # Cambia 'home' por tu vista principal
        else:
            messages.error(request, 'Por favor corrige los errores below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})