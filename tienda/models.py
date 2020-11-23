from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comprador(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()
    imagen = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    @property
    def imagenURL(self):
        try:
            url = self.imagen.url
        except:
            url = ''
        return url


class Pedido(models.Model):
    comprador = models.ForeignKey(Comprador, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    id_transaccion = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def calcular_total_carrito(self):
        articulospedido = self.articulopedido_set.all()
        total = sum([articulo.calcular_total for articulo in articulospedido])
        return total
    
    @property
    def calcular_articulos_carrito(self):
        articulospedido = self.articulopedido_set.all()
        total = sum([articulo.cantidad for articulo in articulospedido])
        return total


class ArticuloPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    @property
    def calcular_total(self):
        total = self.cantidad * self.producto.precio
        return total


class DireccionEnvio(models.Model):
    comprador = models.ForeignKey(Comprador, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=200, null=False)
    ciudad = models.CharField(max_length=200, null=False)
    estado = models.CharField(max_length=200, null=False)
    codigo_postal = models.CharField(max_length=200, null=False)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.direccion
