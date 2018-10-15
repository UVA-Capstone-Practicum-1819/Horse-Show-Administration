from django.contrib import admin
from django.urls import path

from show import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_show', views.create_show, name='create_show'),
]
