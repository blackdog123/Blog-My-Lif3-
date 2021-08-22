from django.contrib import admin
from .models import Post, Profile, Relationship, Comment, Answer, Room, Message

# Register your models here.

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Comment)
admin.site.register(Answer)
admin.site.register(Room)
admin.site.register(Message)