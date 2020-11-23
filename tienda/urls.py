from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name = "tienda"),
    path('carrito/', views.carrito, name = "carrito"),
    path('checkout/', views.checkout, name = "checkout"),
    path('eliminar/<int:id>/', views.eliminar_articulo, name='eliminar_articulo'),
    path('producto/<int:id>/', views.detalles_producto, name='producto'),
    path('agregar/<int:id>/', views.agregar, name='agregar'),
    path('aumentar/<int:id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('disminuir/<int:id>/', views.disminuir, name='disminuir_cantidad'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('tarjeta/', views.tarjeta, name='tarjeta'),
    path('confirmacion/', views.confirmacion, name='confirmacion')
    
]