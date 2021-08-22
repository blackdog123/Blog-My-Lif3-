from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.

permissions_choice = (
    ('Administrador', 'Administrador'),
    ('Usuario', 'Usuario'),
)

verifique_choice = (
    ('Verificado', 'Verificado'),
    ('No Verificado', 'No Verificado'),
)

estate_choice = (
    ('Conectado', 'Conectado'),
    ('Ausente', 'Ausente'),
    ('Desconectado', 'Desconectado'),
)


class Profile(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE)
    bio                     = models.TextField(max_length=255 ,blank=True, null=False)
    foto_perfil             = models.ImageField(default='user_default.png', upload_to='fotos_perfil')
    foto_portada            = models.ImageField(default="banner_default.jpg", upload_to='fotos_portada')
    link_facebook           = models.CharField(max_length=50, null=True, blank=True)
    link_instagram          = models.CharField(max_length=50, null=True, blank=True)
    link_twitter            = models.CharField(max_length=50, null=True, blank=True)
    link_linkedin           = models.CharField(max_length=50, null=True, blank=True)
    tipo_permiso            = models.CharField(max_length=50, null=True, blank=False, default='Usuario', choices=permissions_choice)
    tipo_verificacion       = models.CharField(max_length=50, null=True, blank=False, default='No Verificado', choices=verifique_choice)
    estado_conexion         = models.CharField(max_length=50, null=True, blank=False, default='Conectado', choices=estate_choice)

    
    
    def __str__(self):
        return f'perfil de {self.user.username}'
    
    def Following(self):
        user_ids = Relationship.objects.filter(from_user = self.user)\
                                    .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)
    
    def Followers(self):
        user_ids = Relationship.objects.filter(to_user = self.user)\
                                    .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)



class Post(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    fecha_creacion      = models.DateTimeField(default=timezone.now)
    texto               = models.TextField(blank=True)
    imagen              = models.ImageField(upload_to='imagenes', null=True, blank=False)
    video               = models.FileField(upload_to='videos', blank=False )
    likes               = models.ManyToManyField(User, related_name="blog_posts")

    class Meta:
        ordering = ['fecha_creacion']

    def _str_(self):
        return f'{self.user.username}: {self.content}'
    
    def total_likes(self):
        return self.likes.count()

class Relationship(models.Model):
    from_user           = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
    to_user             = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'

        class Meta:
            indexes = [
                models.Index(fields=['from_user', 'to_user',]),
                ]

class Comment(models.Model):
    post                = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion      = models.DateTimeField(default=timezone.now)
    texto               = models.TextField()

    class Meta:
        ordering = ['fecha_creacion']

    def __str__(self):
        return f'{self.user.username}: comentario post_id {self.post.id}'

class Answer(models.Model):
    comment             = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='answers')
    user                = models.ForeignKey(User, on_delete=models.CASCADE)   
    fecha_creacion      = models.DateTimeField(default=timezone.now)
    texto               = models.TextField()

    class Meta:
        ordering = ['fecha_creacion']

    def __str__(self):
        return f'{self.user.username}: comentario respuesta id {self.comment.id}'

class Room(models.Model):
    name                = models.TextField()
    from_user           = models.ForeignKey(User, default="", related_name='user1', on_delete=models.CASCADE)
    to_user             = models.ForeignKey(User, default="", related_name='user2', on_delete=models.CASCADE)

    def __str__(self):
        return f' chat {self.from_user} and {self.to_user}'

   
 
class Message(models.Model):
    room                = models.ForeignKey(Room, related_name='author_message', on_delete=models.CASCADE)
    author              = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp           = models.DateTimeField(default=timezone.now)   
    content             = models.TextField()

    def __str__(self):
        return self.author.username

    def last_10_messages(self):
        return Message.objects.order_by('.timestamp').all()[:10]

        
            