from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

class_patterns = [
     path('rank',
         views.rank_class, name='rank_class'),

     path('edit',
         views.class_info, name="edit_class"),

     path('delete',
         views.delete_class, name="delete_class"), 
]

division_patterns = [
     path('',
         views.division, name="division_info"),

     path('add-class',
         views.add_class, name="add_class"),

     path('class/<class_num>/', include(class_patterns)),
     
     path('select-class',
         views.class_select, name="select_class"),

     path('division-score',
         views.divisionscore, name="division_score"),

     path('division-classes',
         views.division_classes, name="division_classes"),

     path('class-autocomplete', views.ClassAutocomplete.as_view(),
         name="classes_autocomplete"),
]

combo_patterns = [
     path('delete',
         views.delete_combo, name="delete_combo"),

     path('billing-list',
         views.billinglist, name="billinglist"),

     path('scratch', views.scratch, name="scratch"),

     path('edit', views.edit_combo, name="edit_combo"),
]

show_patterns = [
     path('', views.view_show, name='view_show'),

     path('division/<division_name>/', include(division_patterns)),
     
     path('add-combo', views.add_combo, name="add_combo"),

     path('combo/<combo_num>/', include(combo_patterns)),

     path('add-horse', views.add_horse, name="add_horse"),

     path('add-rider', views.add_rider, name="add_rider"),

     path('add-division', views.add_division, name="add_division"),
    
     path('select-division', views.select_division, name="select_division"),
     
     path('view-billing', views.view_billing, name="view_billing"),

     path('rider/<rider_pk>/edit', views.edit_rider, name="edit_rider"),

     path('horse/<horse_pk>/edit', views.edit_horse, name="edit_horse"),

     path('select-rider', views.select_rider, name="select_rider"),

     path('select-horse', views.select_horse, name="select_horse"),

     path('select-rider2', views.select_rider2, name="select_rider2"),

     path('select-horse2', views.select_horse2, name="select_horse2"),

     path('combo-autocomplete', views.ComboAutocomplete.as_view(),
         name="combo_autocomplete"),
     
     path('division-autocomplete', views.DivisionAutocomplete.as_view(),
         name="division_autocomplete"),

     path('populate-pdf', views.populate_pdf, name="populate_pdf"),
]

urlpatterns = [
    path('', views.show_select, name="show_select"),

    path('<show_date>/', include(show_patterns)),

    path('signup', views.signup, name='sign_up'),

    path('login', auth_views.LoginView.as_view(
        template_name='login.html'), name='log_in'),

    path('logout', auth_views.LogoutView.as_view(), name='log_out'),

    path('add-show', views.create_show, name='add_show'),

    path('show-autocomplete', views.ShowAutocomplete.as_view(),
         name="show_autocomplete"),
    
    path('rider-autocomplete', views.RiderAutocomplete.as_view(),
         name="rider_autocomplete"),

    path('horse-autocomplete', views.HorseAutocomplete.as_view(),
         name="horse_autocomplete"),
    
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

    Most of our url templates show how certain subdivisions exist in the organization of the horse show, so the information
    can be passed between different templatesself
    Obsolete URLs were commented out or removed
    Autocomplete pages are only used for autocomplete functionality- will not be a functional page for the purpose
    of organizing a Horse Show

The URL paths
In the future, we need to split this file up into multiple URL confs in a tree-like fashion so as to better organize and have simpler paths
 """