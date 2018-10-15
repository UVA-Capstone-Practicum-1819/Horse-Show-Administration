from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from show import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_show', views.create_show, name='create_show'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
]
