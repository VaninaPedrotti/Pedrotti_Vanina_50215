from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Libro)
admin.site.register(Comentario)
admin.site.register(Wishlist)