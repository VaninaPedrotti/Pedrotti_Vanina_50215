from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import *
from .forms import * 

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.contrib.auth import logout as django_logout

def home(request):
    return render(request, "aplicacion/index.html")

def acercaDeMi(request):
    return render(request, "aplicacion/acercaDeMi.html")

def pagDefault(request):
    return render(request, "aplicacion/pagDefault.html")

#?________________________ iniciar sesion - cerrar sesion - registrar
def login_request(request):         
    if request.method == "POST":
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            try: 
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.jpg"
            finally:
                request.session["avatar"] = avatar
            return redirect(reverse_lazy('producto'))
        else:
            return redirect(reverse_lazy('login'))
    else:
        miForm = AuthenticationForm()
    
    return render(request, "aplicacion/login.html", {"form": miForm} )

@login_required
def logout(request):
    django_logout(request)
    return redirect(reverse_lazy('home'))

def register(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)

        if miForm.is_valid():
            usuario = miForm.cleaned_data.get("username")
            miForm.save()
            return redirect(reverse_lazy('login'))
    else:
        miForm = RegistroForm()

    return render(request, "aplicacion/registro.html", {"form": miForm} )
    
#?_________________________________Editar perfil - contraseña __ avatar
@login_required
def editProfile(request):
    usuario = request.user
    if request.method == "POST":
        miForm = UserEditForm(request.POST)
        if miForm.is_valid():
            user = User.objects.get(username=usuario)
            user.email = miForm.cleaned_data.get("email")
            user.first_name = miForm.cleaned_data.get("first_name")
            user.last_name = miForm.cleaned_data.get("last_name")
            user.save()
            return redirect(reverse_lazy('producto'))
    else:
        miForm = UserEditForm(instance=usuario)

    return render(request, "aplicacion/editarPerfil.html", {"form": miForm} )    

class CambiarClave(LoginRequiredMixin, PasswordChangeView):
    template_name = "aplicacion/cambiar_clave.html"
    success_url = reverse_lazy("producto")

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        miForm = AvatarForm(request.POST, request.FILES)

        if miForm.is_valid():
            usuario = User.objects.get(username=request.user)
            #___ Borrar avatares viejos
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            #____________________________________________________
            avatar = Avatar(user=usuario,
                            imagen=miForm.cleaned_data["imagen"])
            avatar.save()
            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session["avatar"] = imagen
            
            return redirect(reverse_lazy('home'))
    else:
        miForm = AvatarForm()

    return render(request, "aplicacion/agregarAvatar.html", {"form": miForm} ) 

#?_________________________________Producto = home de los usuarios
#Muestra
class LibroList(LoginRequiredMixin, ListView):
    model = Libro
    context_object_name = 'libros'

class LibroDetalleConComentarios(DetailView):
    model = Libro
    template_name = 'aplicacion/libroDetalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objeto = self.get_object()
        comentarios = objeto.comentarios.all()  # Obtener todos los comentarios relacionados con el objeto
        context['comentarios'] = comentarios
        return context

#Crea
class LibroCreate(LoginRequiredMixin, CreateView):
    model = Libro
    fields = ["titulo", "autor", "descripcion", "precio", "genero", "ubicacion", "imagen"]
    #De automatico guarde el usuario
    def form_valid(self, form):
        form.instance.usuario = self.request.user 
        return super().form_valid(form)

    success_url = reverse_lazy("producto")

#Modifica
class LibroUpdate(LoginRequiredMixin, UpdateView):
    model = Libro
    fields = ["titulo", "autor", "descripcion", "precio", "genero", "ubicacion", "imagen"]
    success_url = reverse_lazy("producto")
    # Filtra los objetos basados en el usuario actual
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user)

#Elimina
class LibroDelete(LoginRequiredMixin, DeleteView):
    model = Libro
    success_url = reverse_lazy("producto")
    # Filtra los objetos basados en el usuario actual
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user)

    # Verifica si el usuario es el creador del objeto antes de eliminarlo
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.usuario == self.request.user:
            return super().delete(request, *args, **kwargs)
        else:
            # Devuelve un error o redirige a otra página
            return rendirect(reverse_lazy("producto"))

#buscar
@login_required
def encontrarLibro(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        libros = Libro.objects.filter(titulo__icontains=patron)
        contexto = {"libros": libros}
        return render(request, "aplicacion/libro_list.html", contexto)
    
    contexto = {'libros': Libro.objects.all()}
    return render(request, "aplicacion/libro_list.html", contexto) 

#?________________________Comentario
class ComentarioList(LoginRequiredMixin,ListView):
    model = Comentario
    template_name = 'aplicacion/libroDetalle.html'
    context_object_name = 'comentarios'

class ComentarioCreate(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'aplicacion/agregar_comentario.html'

    #para que guarde el usuario y el id del objeto que esta comentanto
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.objeto_comentado_id = self.kwargs['pk']  # Obtener el ID del objeto comentado de la URL
        return super().form_valid(form)
    
    #para que redirija al objeto pasandole el id
    def get_success_url(self):
        return reverse_lazy('libro_detalle', kwargs={'pk': self.kwargs['pk']})

class ComentarioUpdate(LoginRequiredMixin, UpdateView):
    model = Comentario
    fields = ["mensaje"]
    success_url = reverse_lazy("producto")
    template_name = 'aplicacion/agregar_comentario.html'
    # Filtra los objetos basados en el usuario actual
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user)


class ComentarioDelete(LoginRequiredMixin, DeleteView):
    model = Comentario
    success_url = reverse_lazy("producto")
    # Filtra los objetos basados en el usuario actual
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user)

    # Verifica si el usuario es el creador del objeto antes de eliminarlo
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.usuario == self.request.user:
            return super().delete(request, *args, **kwargs)
        else:
            # Devuelve un error o redirige a otra página
            return rendirect(reverse_lazy("producto"))


#?________________________Lista de deseos
@login_required
def lista_deseos(request):
    wishlist = Wishlist.objects.filter(usuario=request.user).first()
    libros = wishlist.libros.all() if wishlist else []
    return render(request, 'aplicacion/wishlist.html', {'libros': libros})

@login_required
def agregar_a_wishlist(request, libro_id):
    if request.method == 'POST':
        usuario = request.user
        libro = Libro.objects.get(pk=libro_id)
        wishlist, created = Wishlist.objects.get_or_create(usuario=usuario)
        wishlist.libros.add(libro)
        return redirect('wishlist')
    else:
        return redirect('inicio')

@login_required
def eliminar_de_wishlist(request, libro_id):
    libro = Libro.objects.get(pk=libro_id)
    wishlist = Wishlist.objects.filter(libros=libro).first()
    if wishlist:
        wishlist.libros.remove(libro)
    return redirect('wishlist')


