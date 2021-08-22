from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models.fields import TextField

from django.forms import ModelForm, fields, widgets
#from django.urls.base import reverse
from .models import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
'email', 'password1', 'password2',)


class EditarPerfil(ModelForm):

    class Meta:
        model = Profile
        fields = ('foto_perfil','foto_portada' ,'bio', )

        widgets = {
            'foto_perfil':       forms.FileInput(),
            'foto_portada':      forms.FileInput(),
            'bio':               forms.Textarea(attrs={'rows':2, 'placeholder':'Escribe una descripción sobre ti'}),
        }
    

class EditarInfo(UserChangeForm):

    username =        forms.CharField(label="Nombre Usuario")
    first_name =      forms.CharField(label="Nombre" , widget=forms.TextInput(attrs={'placeholder':''}), required=False)
    last_name =       forms.CharField(label="Apellido" , widget=forms.TextInput(attrs={'placeholder':''}), required=False)
    email =           forms.CharField(label="Email")
    
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'password',)


class EditBio(ModelForm):
    bio = forms.CharField(label="Mi Descripción", widget=forms.Textarea(attrs={'rows':4,'placeholder':'Escribe algúna descripción o algo sobre tí'}))

    class Meta:
        model = Profile
        fields = ('bio',)

        
class PasswordChangingForm(PasswordChangeForm):

    old_password =       forms.CharField(label='Contraseña Actual', widget=forms.PasswordInput(attrs={'type':'password', 'placeholder':'Escribe aquí tú contraseña actual'}))
    new_password1 =      forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput(attrs={'type':'password', 'placeholder':'Escribe aquí tú nueva contraseña'}))
    new_password2 =      forms.CharField(label='Confirmar Nueva Contraseña', widget=forms.PasswordInput(attrs={'type':'password', 'placeholder':'Confirma aquí tú nueva contraseña'}))
    
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2',)


class EditarPost(ModelForm):
    texto = forms.CharField(label="", widget=forms.Textarea(attrs={'rows':4, 'placeholder': 'Escribe aquí algo sobre tu post'}), required=False )

    class Meta:
        model = Post
        fields = ('texto',)

class CreateRoom(ModelForm):
    name    = forms.CharField(label="", widget=forms.TextInput(attrs={'rows':2, 'placeholder': 'Nombre de la Sala'}), required=True )

    class Meta:
        model = Room
        fields = ('name',)



#class SubirImagen(ModelForm):

#    class Meta:
#        model = Post
#        fields = ('user','texto', 'imagen')

#        widgets = {
#            'user':         forms.TextInput(attrs=({'value':'', 'id':'elder', 'type':'hidden'})),
#            'texto':        forms.Textarea(attrs=({'placeholder': 'Escribe aquí algo sobre tú imagen', 'rows':4 })),
#            'imagen':       forms.FileInput(attrs=({'accept':'image/png, image/gif, image/jpeg'}))
       
#        }

class SubirVideo(ModelForm):

    class Meta:
        model = Post
        fields = ('user','texto', 'video')

        widgets = {
            'user':         forms.TextInput(attrs=({'value':'', 'id':'elder', 'type':'hidden'})),
            'texto':        forms.Textarea(attrs=({'placeholder': 'Escribe aquí algo sobre tú video', 'rows':4 })),
            'video':       forms.FileInput(attrs=({'accept':'video/mp4,video/x-m4v,video/*'}))
            
       
        }



# models dashboard



class EditarUsuario(ModelForm):

    username           = forms.CharField(help_text='', label='Nombre de Usuario', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    first_name         = forms.CharField(help_text='', label='Nombre' ,widget=forms.TextInput(attrs={'readonly':'readonly'}))
    last_name          = forms.CharField(help_text='', label='Apellido' ,widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email              = forms.CharField(help_text='', label='Email' ,widget=forms.TextInput(attrs={'type':'email','readonly':'readonly'}))
    is_active          = forms.CharField(label="Activo", widget=forms.CheckboxInput(attrs={}), required=False)

    class Meta:
        model = User 
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active',)


class EditarPermiso(ModelForm):

    class Meta:
        model = Profile
        fields = ('tipo_permiso', 'tipo_verificacion',)