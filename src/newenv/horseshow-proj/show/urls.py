
from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_show', views.create_show, name='create_show'),

    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    # path('admin/', admin.site.urls),
    path('horse/new', views.horse_new, name="horse_new"),
    path('rider/new', views.newrider, name="newrider"),
    path('class/new', views.new_class, name="classes"),
    path('horse', views.horse_select, name="horse_select"),
    path('show', views.show_select, name="show_select"),
    path('billing', views.billing, name="billing"),
    path('show-autocomplete', views.ShowAutocomplete.as_view(), name="show_autocomplete"),
    path('rider', views.rider_select, name="rider_select"),
    path('rider-autocomplete', views.RiderAutocomplete.as_view(), name="rider_autocomplete"),
    path('horse-autocomplete', views.HorseAutocomplete.as_view(), name="horse_autocomplete"),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('addcombo', views.add_combo, name="addcombo"),
    path('addcombo/newcombo', views.add_combo, name="newcombo")


]
"""horseshow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
