from collections import namedtuple
from django.conf.urls import url
from django.contrib.auth import views as auth_views 
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url

from django_filters.views import FilterView
from .filters import UserFilter

from .views import Comentarios, DeletePostView, LikeView, ChatView, Room, EditarPerfilView, ConfigView, AddVideoView, ExplorarView, UpdatePostView, DeletePostView, PasswordsChangeView

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

path('', views.index, name='index'),
path('usuarios', views.usuarios, name='usuarios'),
path('explorar', ExplorarView.as_view(), name='explorar'),
path('comentarios/<int:pk>', Comentarios.as_view(), name='comentarios'),

#---------------------------------------------------------------
# url login , logout and signup
#---------------------------------------------------------------
path('login', views.login, name='login'),
path('logout', views.logout, name='logout'),
path('registro', views.registro, name='registro'),

#---------------------------------------------------------------
# Vitas Perfil
#---------------------------------------------------------------

path('perfil/<str:username>/', views.perfil, name='perfil'),
path('editar_perfil/<int:pk>', EditarPerfilView.as_view(), name='editar_perfil'),
path('configuracion/<int:pk>', ConfigView.as_view(), name='configuracion'),
path('password/', PasswordsChangeView.as_view(template_name='chage-password.html')),


path('crear_sala', views.crear_sala, name='crear_sala'),
path('crear_mensaje/<int:pk>', views.crear_mensaje, name='crear_mensaje'),
path('chat', ChatView.as_view(), name='chat'),
path('room/<int:pk>', Room.as_view(), name='room'),

#---------------------------------------------------------------
# url forms posts and accions
#---------------------------------------------------------------

path('upload_post', views.upload_post, name='upload_post'),
path('upload_image', views.upload_image, name='upload_image'),
#path('subir_imagen', AddImageView.as_view(), name='subir_imagen'),
path('subir_video', AddVideoView.as_view(), name='subir_video'),

path('follow/<str:username>/', views.follow, name='follow'),
path('unfollow/<str:username>/', views.unfollow, name='unfollow'),

path('editar_post/<int:pk>', UpdatePostView.as_view(), name='editar_post'),
path('eliminar_post/<int:pk>', DeletePostView.as_view(), name='eliminar_post'),

path('publicar_comentario/<int:pk>', views.publicar_comentario, name='publicar_comentario'),
path('publicar_respuesta/<int:pk>', views.publicar_respuesta, name='publicar_respuesta'),
path('like/<int:pk>', LikeView, name='like_post'),


#---------------------------------------------------------------
# url dashboard
#---------------------------------------------------------------

path('dashboard', views.dashboard, name='dashboard'),
path('users', views.users, name='users'),
path('eliminar_post_dashboard/<int:id>', views.eliminar_post_dashboard, name='eliminar_post_dashboard'),
path('editar_usuario/<int:id>', views.editar_usuario, name='editar_usuario'),
path('editar_permiso/<int:id>', views.editar_permiso, name='editar_permiso'),
path('eliminar_usuario/<int:id>', views.eliminar_usuario, name='eliminar_usuario'),



#reset passwords templates
path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
 
path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
 
path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
 
path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]