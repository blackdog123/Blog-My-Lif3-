from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.views.generic.base import View
from django.views.generic.edit import DeleteView
from .forms import SignUpForm, EditarPerfil, EditarInfo, EditarPost, CreateRoom, SubirVideo, EditarUsuario, EditarPermiso, PasswordChangingForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
import time
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import UserFilter, DashBoardUserFilter
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required


# Create your views here.

#--------------------------------------------------------------------
# Feed, Users and Explorer
#--------------------------------------------------------------------


def index(request):
 
    users = User.objects.all().order_by("-id")[:6]
    posts = Post.objects.all().order_by("-fecha_creacion")
     
    context = {'users':users, 'posts':posts}
    return render(request, 'index.html', context)


def usuarios(request):
    if request.user.is_authenticated:
        user_list = User.objects.all().order_by("-id")
        user_filter = UserFilter(request.GET, queryset=user_list)
        return render(request, 'usuarios.html', {'filter': user_filter})
    else:
        return redirect('/login')


class ExplorarView(LoginRequiredMixin, ListView): 
    model = Post
    template_name = 'explorar.html'
    ordering = ['-id'] 

    login_url = '/login'

#--------------------------------------------------------------------
# End Home and Users
#--------------------------------------------------------------------



#--------------------------------------------------------------------
# Change Password
#--------------------------------------------------------------------

class PasswordsChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm 
    #form_class = PasswordChangeForm

    success_message = "Tú contraseña se cambio correctamente"
    success_url = reverse_lazy('index')
    login_url = '/login'


#--------------------------------------------------------------------
# End Change Password
#--------------------------------------------------------------------



#--------------------------------------------------------------------
# Chat, Room and create message
#--------------------------------------------------------------------
        

class ChatView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'chat.html'

    login_url = '/login'
 


class Room(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'room.html'

    login_url = '/login'


def crear_mensaje(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            mi_author = request.POST['author_id']
            mi_room = request.POST['room_id']
            mi_content = request.POST['content']
            
            if  mi_content != "":
                try:
                    
                    message = Message()

                    message.author_id  = mi_author
                    message.room_id = mi_room
                    message.content = mi_content
                    message.activo = 1

                    message.save()
                    
                    return HttpResponseRedirect(reverse('room', args=[str(pk)]))
                    
                
                except message.DoesNotExist:
                   return HttpResponseRedirect(reverse('room', args=[str(pk)]))
            
            else:
                messages.error(request, "Error ! tú mensaje no pudo ser enviado, por favor intentalo nuevamente")
                return HttpResponseRedirect(reverse('room', args=[str(pk)]))
        
        else:
            return HttpResponseRedirect(reverse('room', args=[str(pk)]))
    
    else: 
        return HttpResponseRedirect(reverse('room', args=[str(pk)]))   


def crear_sala(request):
    # Creamos un formulario vacío
    form = CreateRoom()

    if request.method == "POST":
      
        form = CreateRoom(request.POST)
   
        if form.is_valid():
         
            instancia = form.save(commit=False)
   
            instancia.save()
         
            return redirect('/chat')

    return render(request, "crear_sala.html", {'form': form})

#--------------------------------------------------------------------
# End Chat, Room and create message
#--------------------------------------------------------------------



#--------------------------------------------------------------------
# Like Post
#--------------------------------------------------------------------

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True 

    return HttpResponseRedirect(reverse('comentarios', args=[str(pk)]))

#--------------------------------------------------------------------
# End Like Post
#--------------------------------------------------------------------




#--------------------------------------------------------------------
# Comment view Post
#--------------------------------------------------------------------
 
class Comentarios(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'comentarios.html'
    login_url = '/login'
    
    
    def get_context_data(self, *args, **kwargs):
        context = super(Comentarios, self).get_context_data(*args, **kwargs)

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True    


        context["total_likes"] = total_likes 
        context["liked"] = liked
        return context


#---------------------------------------------------------
#   Login, Logout, Signup
#----------------------------------------------------------

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)

            return redirect('/')
        else:
            messages.error(request, "Error ! Verifique Bien su Usuario y Contraseña")
            return redirect('/login')
            
    return render(request, "login.html", {'form': form})

 

def logout(request):
    do_logout(request)
    return redirect('/')
  


def registro(request):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            do_login(request, user)
            messages.success(request, f'Bienvenido {username}')
            return redirect('/')
        else:
            messages.error(request, "No se pudo crear el usuario Correctamente, puede que ya exista alguien con ese nombre de usuario, o la contraseña es muy debíl, por favor intentalo nuevamente")
            return redirect('/registro')

    form = SignUpForm()
    return render(request, 'registro.html', {'form': form})


#--------------------------------------------------------------------
# End login , logout and Signup 
#--------------------------------------------------------------------


#---------------------------------------------------------
#   upload Post, image and video
#----------------------------------------------------------
    
def upload_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            mi_user = request.POST['user_id']
            mi_texto = request.POST['texto']
            
            if mi_user != "":
                try:
                    
                    post = Post()

                    post.user_id  = mi_user
                    post.texto = mi_texto
                    post.activo = 1

                    post.save()
                    
                    messages.success(request, 'Tú post se publicó correctamente')
                    return redirect( '/')
                    
                except post.DoesNotExist:
                    messages.error(request, 'Tú post no se pudo publicar, por favor intentalo nuevamente')
                    return redirect('/')
            
            else:
                messages.error(request, 'Tu post no se pudo publicar, por favor intentalo nuevamente')
                return redirect('/')
        
        else:
            messages.error(request, 'El metodo post no es correcto')
            return redirect('/')
    
    else: 
        return redirect('/login')   



def upload_image(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            mi_user = request.POST['user_id']
            mi_texto = request.POST['texto']
            mi_imagen = request.FILES['imagen']
            
            if mi_imagen != "":
                try:
                    
                    post = Post()

                    post.user_id  = mi_user
                    post.texto = mi_texto
                    post.imagen = mi_imagen
                    post.activo = 1

                    post.save()
                    
                    messages.success(request, 'Tú imagen se publicó Correctamente')
                    return redirect( '/')
                    
                except post.DoesNotExist:
                    messages.error(request, 'Tú imagen no se pudo publicar, por favor intentalo nuevamente')
                    return redirect('/')
            
            else:
                messages.error(request, 'Tú imagen no se pudo publicar, por favor intentalo nuevamente')
                return redirect('/')
        
        else:
            messages.error(request, 'El metodo post no es correcto')
            return redirect('/')
    
    else: 
        return redirect('/login')   

        
class AddVideoView(SuccessMessageMixin, LoginRequiredMixin, CreateView):

    model = Post
    template_name = 'subir_video.html'
    form_class = SubirVideo

    success_message = "Tú video se publicó con exito"
    success_url = reverse_lazy('index')
    login_url = '/login'

#----------------------------------------------------------
#   End upload Posts
#----------------------------------------------------------



#---------------------------------------------------------
#   update and delete Posts
#---------------------------------------------------------

class UpdatePostView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'editar_post.html'
    form_class = EditarPost
    success_url = reverse_lazy = ('/')
    success_message = "Tú publicación se editó correctamente"
    login_url = '/login'


class DeletePostView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'eliminar_post.html'

    success_url = reverse_lazy = ('/')
    success_message = "Tú publicación se eliminó correctamente"
    login_url = '/login'


#---------------------------------------------------------
#   End update and delete Posts
#---------------------------------------------------------



#---------------------------------------------------------
#   Public New Comment and Answer
#---------------------------------------------------------
    
def publicar_comentario(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            mi_post = request.POST['post_id']
            mi_user = request.POST['user_id']
            mi_texto = request.POST['texto']
            
            if mi_texto != "" :
                try:
                    
                    comment = Comment()

                    comment.post_id  = mi_post 
                    comment.user_id  = mi_user 
                    comment.texto = mi_texto
                    comment.activo = 1

                    comment.save()
                
                    return HttpResponseRedirect(reverse('comentarios', args=[str(pk)]))
                    
                except comment.DoesNotExist:
                    messages.error(request, 'Tú comentario no se pudo publicar, por favor intententalo nuevamente')
                    return HttpResponseRedirect(reverse('comentarios', args=[str(pk)]))
            
            else:
                messages.error(request, 'lo sentimos, tú comentario no se pudo publicar, por favor intententalo nuevamente ')
                return HttpResponseRedirect(reverse('comentarios', args=[str(pk)]))
        
        else:
            messages.error(request, 'El metodo post es incorrecto ')
            return HttpResponseRedirect(reverse('comentarios', args=[str(pk)]))
    
    else: 
        return redirect('/login')   
   

def publicar_respuesta(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            mi_comment = request.POST['comment_id']
            mi_user = request.POST['user_id']
            mi_texto = request.POST['texto']
            
            if mi_texto != "" :
                try:
                    
                    answer = Answer()

                    answer.comment_id  = mi_comment 
                    answer.user_id  = mi_user 
                    answer.texto = mi_texto
                    answer.activo = 1

                    answer.save()
                    
                    return HttpResponseRedirect(reverse('comentarios', args=[str(pk)]))

                except answer.DoesNotExist:
                    messages.error(request, 'Tú comentario no se pudo publicar, por favor intententalo nuevamente')
                    return HttpResponseRedirect(reverse('comentarios', args=[str(pk)]))
            
            else:
                messages.error(request, 'lo sentimos, tú comentario no se pudo publicar, por favor intententalo nuevamente ')
                return HttpResponseRedirect(reverse('comentarios', args=[str(pk)]))
        
        else:
            messages.error(request, 'El metodo post es incorrecto ')
            return HttpResponseRedirect(reverse('comentarios', args=[str(pk)]))
    
    else: 
        return redirect('/login')  

#---------------------------------------------------------
#   End Public New Comment
#---------------------------------------------------------



#---------------------------------------------------------
#   Profile
#---------------------------------------------------------

@login_required(login_url='/login')   
def perfil(request, username=None):
  
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all().order_by('-fecha_creacion')
    else:
        posts = current_user.posts.all().order_by('-fecha_creacion')
        user = current_user

    return render(request, 'perfil.html', {'user':user, 'posts':posts})


#---------------------------------------------------------
#   End Profile
#---------------------------------------------------------
      
  

#--------------------------------------------------------------------
# Update Profile
#--------------------------------------------------------------------

class EditarPerfilView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'editar_perfil.html'
    form_class = EditarPerfil

    success_message = "Tú perfil se editó correctamente"
    success_url = "/"
    login_url = '/login'

  

class ConfigView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'configuracion.html'
    form_class = EditarInfo

    success_message = "Tú configuración se editó correctamente"
    success_url = "/"
    login_url = '/login'


#--------------------------------------------------------------------
# End Update Profile
#--------------------------------------------------------------------




#---------------------------------------------------------
#   Action Follow and Unfollow
#---------------------------------------------------------


def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'Sigues a {username}')
    return HttpResponseRedirect(reverse('perfil', args=[str(username)]))

def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'Dejaste de seguir a {username}')
    return HttpResponseRedirect(reverse('perfil', args=[str(username)]))



#---------------------------------------------------------
#   Dashboard
#---------------------------------------------------------

        
def dashboard(request):
    if request.user.is_authenticated: 
        users = User.objects.all()
        posts = Post.objects.all()
        comments = Comment.objects.all()
        answers = Answer.objects.all()
        context = {'users':users, 'posts':posts, 'comments':comments,'answers':answers}
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return redirect('/login')



def users(request):
    if request.user.is_authenticated:
        user_list = User.objects.all()
        user_filter = DashBoardUserFilter(request.GET, queryset=user_list)
        return render(request, 'dashboard/users.html', {'filter': user_filter})
    else:
        return redirect('/login')



def eliminar_post_dashboard(request, id):
    instancia = Post.objects.get(id=id)
    instancia.delete()

    messages.success(request, 'Se eliminó la publicación correctamente')
    return redirect('/dashboard')


@login_required(login_url='/login')   
def editar_usuario(request, id):

    instancia = User.objects.get(id=id)
    form = EditarUsuario(instance=instancia)

    if request.method == "POST":
     
        form = EditarUsuario(request.POST, instance=instancia)

        if form.is_valid():
    
            instancia = form.save(commit=False)
     
            instancia.save()

            messages.success(request, 'Se editó el usuario correctamente')
            return redirect('/users')

        else:

            messages.error(request, 'No se pudo editar el usuario, por favor intentalo nuevamente')
            return redirect(request, '/editar_usuario')


    return render(request, "dashboard/editar_usuario.html", {'form': form})


@login_required(login_url='/login')   
def editar_permiso(request, id):

    instancia = Profile.objects.get(id=id)
    form = EditarPermiso(instance=instancia)

    if request.method == "POST":
     
        form = EditarPermiso(request.POST, instance=instancia)

        if form.is_valid():
    
            instancia = form.save(commit=False)
     
            instancia.save()

            messages.success(request, 'Se editó el permiso del usuario correctamente')
            return redirect('/users')

        else:

            messages.error(request, 'No se pudo editar el permiso del usuario, por favor intentalo nuevamente')
            return redirect(request, '/editar_permiso')


    return render(request, "dashboard/editar_permiso.html", {'form': form})


@login_required(login_url='/login')
def eliminar_usuario(request, id):
    if request.user.is_authenticated:
        instancia = User.objects.get(id=id)
        instancia.delete()

        messages.success(request, 'Se eliminó el usuario correctamente')
        return redirect('/users')
    else:
        return redirect('/login')



