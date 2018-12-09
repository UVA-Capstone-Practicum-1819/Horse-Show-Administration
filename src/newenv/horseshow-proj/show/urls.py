from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('create_show', views.create_show, name='create_show'),
    path('showpage/<showdate>', views.showpage, name='showpage'),
    path('<classname>/rankclass', views.rankclass, name='rankclass'),
    path('horse/new', views.add_horse, name="add_horse"),
    path('rider/new', views.add_rider, name="add_rider"),
    path('class/new', views.new_class, name="classes"),
    path('<showdate>/<divisionname>', views.division, name="division_info"),
    # path('<showdate>/<divisionname>/classes', views.division, name="division_info"),    
    path('<showdate>/division/new', views.new_division, name="divisions"),
    path('horse', views.select_horse, name="select_horse"),
    path('show', views.show_select, name="show_select"),
    path('class', views.class_select, name="class_select"),
    path('<showdate>/division', views.division_select, name="division_select"),
    path('<divisionname>/divisionscore',
         views.divisionscore, name="divisionscore"),
    path('<divisionname>/division_classes',
         views.division_classes, name="division_classes"),
    path('<divisionname>/<classname>/delete_class',
         views.delete_class, name="delete_class"),
    path('<showdate>/billing', views.billing, name="billing"),
    path('<showdate>/<combonum>/billinglist',
         views.billinglist, name="billinglist"),
    path('<showdate>/<combonum>/scratch', views.scratch, name="scratch"),
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
    path('add-combo', views.add_combo, name="add_combo"),
    path('combo/<num>', views.edit_combo, name="edit_combo"),

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
