from django.urls import path, include
from .views import *

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name="home"),
    path('about', acercaDeMi, name="about"),
    path('default', pagDefault, name="pagina_default"),

    path('login/', login_request, name="login"),
    path('logout/', logout, name="logout"),
    path('registrar/', register, name="registrar"),

    path('perfil/', editProfile, name="perfil"),
    path('<int:pk>/password/', CambiarClave.as_view(), name="cambiar_clave"),
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar"),

    path('productos/', LibroList.as_view(), name="producto"), 
    path('libroDetalleConComentarios/<int:pk>/', LibroDetalleConComentarios.as_view(), name='libro_detalle'),    
    path('libro_crear/', LibroCreate.as_view(), name="libro_crear"), 
    path('libro_modificar/<int:pk>/', LibroUpdate.as_view(), name="libro_modi"), 
    path('libro_eliminar/<int:pk>/', LibroDelete.as_view(), name="libro_eliminar"), 
    path('encontrar_libro/', encontrarLibro, name="encontrar_libro"),

    path('libroDetalle/<int:pk>/comentario/', ComentarioCreate.as_view(), name="agregar_comentario"),
    path('comentario_modificar/<int:pk>/', ComentarioUpdate.as_view(), name="comentario_modi"), 
    path('comentario_eliminar/<int:pk>/', ComentarioDelete.as_view(), name="comentario_eliminar"),

    path('wishlist', lista_deseos, name="wishlist"),
    path('agregar_wishlist/<int:libro_id>/', agregar_a_wishlist, name="agregar_wishlist"),
    path('eliminar_wishlist/<int:libro_id>/', eliminar_de_wishlist, name='eliminar_wishlist'),
]