from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_show', views.create_show, name='create_show'),
    path('<showdate>/showpage', views.showpage, name='showpage'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('horse/new', views.add_horse, name="add_horse"),
    path('rider/new', views.add_rider, name="add_rider"),
    path('class/new', views.new_class, name="classes"),
    path('<showname>/division/new', views.new_division, name="divisions"),
    path('horse', views.select_horse, name="select_horse"),
    path('show', views.show_select, name="show_select"),
    path('class', views.class_select, name="class_select"),
    path('<showname>/division', views.division_select, name="division_select"),
    path('billing', views.billing, name="billing"),
    path('<combonum>/billinglist', views.billinglist, name="billinglist"),
    path('scratch', views.scratch, name="scratch"),
    path('show-autocomplete', views.ShowAutocomplete.as_view(),
         name="show_autocomplete"),
    path('rider', views.select_rider, name="select_rider"),
    path('rider-autocomplete', views.RiderAutocomplete.as_view(),
         name="rider_autocomplete"),
    path('horse-autocomplete', views.HorseAutocomplete.as_view(),
         name="horse_autocomplete"),
    path('class_autocomplete', views.ClassAutocomplete.as_view(),
         name="classes_autocomplete"),
    path('combo_autocomplete', views.ComboAutocomplete.as_view(),
         name="combo_autocomplete"),
    path('division_autocomplete', views.DivisionAutocomplete.as_view(),
         name="division_autocomplete"),
    path('genpdf', views.populate_pdf, name="populate_pdf"),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('add-combo', views.add_combo, name="add_combo"),
    path('combo', views.combo, name="combo"),
    path('combo/<num>', views.check_combo, name="check_combo"),
    path('<showname>', views.viewshow, name="viewshow"),
    path('<showname>/edit', views.edit_show, name="edit_show"),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
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
