from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

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
urlpatterns = [
    path('', views.show_select, name="show_select"),

    path('signup', views.signup, name='signup'),

    path('login', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),

    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    path('create_show', views.create_show, name='create_show'),

    path('showpage/<show_date>', views.showpage, name='showpage'),

    path('<show_date>/<division_name>/<class_num>/rank',
         views.rank_class, name='rank_class'),

    path('<show_date>/add-horse', views.add_horse, name="add_horse"),

    path('<show_date>/add-rider', views.add_rider, name="add_rider"),

    path('<show_date>/<division_name>/add-class',
         views.add_class, name="add_class"),

    path('<show_date>/<division_name>',
         views.division, name="division_info"),

    path('<show_date>/<division_name>/<class_num>/edit',
         views.class_info, name="edit_class"),

    path('<show_date>/<combonum>/delete',
         views.delete_combo, name="delete_combo"),
    path('<show_date>/create_division', views.new_division, name="divisions"),

    path('<show_date>/select-horse', views.select_horse, name="select_horse"),

    path('<show_date>/<division_name>/select_class',
         views.class_select, name="select_class"),

    path('<show_date>/select_division',
         views.division_select, name="division_select"),

    path('<division_name>/divisionscore',
         views.divisionscore, name="divisionscore"),

    path('<division_name>/division_classes',
         views.division_classes, name="division_classes"),

    path('<show_date>/<division_name>/<class_num>/delete_class',
         views.delete_class, name="delete_class"),
    path('<show_date>/billing', views.billing, name="billing"),

    path('<show_date>/<combonum>/billinglist',
         views.billinglist, name="billinglist"),

    path('<show_date>/<combonum>/scratch', views.scratch, name="scratch"),
    path('show-autocomplete', views.ShowAutocomplete.as_view(),
         name="show_autocomplete"),
    path('<show_date>/rider', views.select_rider, name="select_rider"),
    path('<show_date>/select-rider', views.select_rider2, name="select_rider2"),
    path('<show_date>/select-horse', views.select_horse2, name="select_horse2"),
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

    path('<show_date>/add-combo', views.add_combo, name="add_combo"),

    path('<show_date>/combo/<num>', views.edit_combo, name="edit_combo"),

    path('<show_date>/rider/<rider_pk>', views.edit_rider, name="edit_rider"),

    path('<show_date>/horse/<horse_pk>', views.edit_horse, name="edit_horse")
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
