from django.contrib.auth.models import User
import django_filters
from django import forms 

from .models import *


class UserFilter(django_filters.FilterSet):
    username   = django_filters.CharFilter(lookup_expr='icontains', label="Nombre de Usuario")
    first_name = django_filters.CharFilter(lookup_expr='icontains', label="Nombre" )
    last_name  = django_filters.CharFilter(lookup_expr='icontains', label="Apellido")

    model = User
    fields = ['username', 'first_name', 'last_name',]



class DashBoardUserFilter(django_filters.FilterSet):
    username   = django_filters.CharFilter(lookup_expr='icontains', label="Nombre de Usuario")
    first_name = django_filters.CharFilter(lookup_expr='icontains', label="Nombre" )
    last_name  = django_filters.CharFilter(lookup_expr='icontains', label="Apellido")
    email      = django_filters.CharFilter(lookup_expr='icontains', label="Email")

    model = User
    fields = ['username', 'first_name', 'last_name', 'email',]

