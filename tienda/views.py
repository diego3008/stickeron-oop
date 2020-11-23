from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate

from .models import *


# Create your views here.

def tienda(request):
    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido, creado = Pedido.objects.get_or_create(
        comprador=comprador, completado=False)
        articulosCarrito = pedido.calcular_articulos_carrito
    else:
        articulos = []
        pedido = {'calcular_total_carrito': 0, 'calcular_articulos_carrito': 0}
        articulosCarrito = pedido['calcular_articulos_carrito']
    
    productos = Producto.objects.all()
    contexto = {'productos': productos, 'articulosCarrito': articulosCarrito}
    return render(request, 'tienda/tienda.html', contexto)


def carrito(request):
    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido, creado = Pedido.objects.get_or_create(
        comprador=comprador, completado=False)
        articulos = pedido.articulopedido_set.all()
        articulosCarrito = pedido.calcular_articulos_carrito
    else:
        articulos = []
        pedido = {'calcular_total_carrito': 0, 'calcular_articulos_carrito': 0}
        articulosCarrito = pedido['calcular_articulos_carrito']
        
    contexto = {'articulos': articulos, 'pedido': pedido, 'articulosCarrito': articulosCarrito}
    return render(request, 'tienda/carrito.html', contexto)


def checkout(request):
    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido, creado = Pedido.objects.get_or_create(
        comprador=comprador, completado=False)
        articulos = pedido.articulopedido_set.all()
        articulosCarrito = pedido.calcular_articulos_carrito
    else:
        articulos = []
        pedido = {'calcular_total_carrito': 0, 'calcular_articulos_carrito': 0}
        articulosCarrito = pedido['calcular_articulos_carrito']

    contexto = {'articulos': articulos, 'pedido': pedido, 'articulosCarrito': articulosCarrito}
    return render(request, 'tienda/checkout.html', contexto)

def eliminar_articulo(request, id):
    articulo = ArticuloPedido.objects.get(pk=id)
    articulo.delete()
    return redirect('carrito')

def aumentar_cantidad(request, id):
    articulo = ArticuloPedido.objects.get(pk=id)
    articulo.cantidad = (articulo.cantidad + 1)
    articulo.save()
    return redirect('carrito')

def disminuir(request, id):
    articulo = ArticuloPedido.objects.get(pk=id)
    articulo.cantidad = (articulo.cantidad - 1)
    if articulo.cantidad == 0:
        articulo.delete()
        return redirect('carrito')
    else:
        articulo.save()
    return redirect('carrito')

def detalles_producto(request, id):
    producto = Producto.objects.get(pk=id)
    contexto = {'producto':producto}
    return render(request, 'tienda/producto.html', contexto)

def agregar(request, id):
    comprador = request.user.comprador
    producto = Producto.objects.get(pk=id)
    pedido, creado = Pedido.objects.get_or_create(comprador=comprador, completado=False)
    
    articulo_pedido, creado = ArticuloPedido.objects.get_or_create(pedido=pedido, producto=producto)
    articulo_pedido.cantidad = (articulo_pedido.cantidad + 1)
    articulo_pedido.save()
    return redirect('carrito')

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('tienda')

    # Si llegamos al final renderizamos el formulario
    return render(request, "tienda/login.html", {'form': form})

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Creamos la nueva cuenta de usuario
            user = form.save()
            comprador = Comprador.objects.get_or_create(usuario=user, nombre=user)
            cliente = Comprador.objects.get(nombre = user.username)
            pedido = Pedido.objects.get_or_create(comprador=cliente, completado=False, id_transaccion=user.username + str(2020))
            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('tienda')    
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    # Si llegamos al final renderizamos el formulario
    return render(request, "tienda/registro.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('tienda')

def tarjeta(request):
    return render(request, 'tienda/tarjeta.html')

def confirmacion(request):
    return render(request, 'tienda/confirmacion.html')

class HomePageView(TemplateView):
    template_name = 'checkout.html'