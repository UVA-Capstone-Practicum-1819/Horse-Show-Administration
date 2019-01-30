from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

class_patterns = [
    path('',
         views.view_class, name="view_class"),

    path('rank',
         views.rank_class, name='rank_class'),

    path('delete',
         views.delete_class, name="delete_class"),

    path('combo/<combo_num>/delete', views.delete_combo, name="delete_combo")
]

division_patterns = [
    path('',
         views.view_division, name="view_division"),

    path('class/add',
         views.add_class, name="add_class"),

    path('class/select',
         views.select_class, name="select_class"),

    path('class/<class_num>/', include(class_patterns)),

    path('scores',
         views.view_division_scores, name="view_division_scores"),

    path('classes',
         views.view_division_classes, name="view_division_classes"),

    path('class-autocomplete', views.ClassAutocomplete.as_view(),
         name="classes_autocomplete"),
]

combo_patterns = [
    path('billing',
         views.view_billing, name="view_billing"),

    path('scratch', views.scratch_combo, name="scratch_combo"),

    path('edit', views.edit_combo, name="edit_combo"),
]

show_patterns = [
    path('', views.view_show, name='view_show'),

    path('division/add', views.add_division, name="add_division"),

    path('division/select', views.select_division, name="select_division"),

    path('division/<division_name>/', include(division_patterns)),

    path('combo/add', views.add_combo, name="add_combo"),

    path('combo/select', views.select_combo, name="select_combo"),

    path('combo/<combo_num>/', include(combo_patterns)),

    path('rider/add', views.add_rider, name="add_rider"),

    path('rider/select', views.select_rider, name="select_rider"),

    path('rider/select2', views.select_rider2, name="select_rider2"),

    path('rider/<rider_pk>/edit', views.edit_rider, name="edit_rider"),

    path('horse/add', views.add_horse, name="add_horse"),

    path('horse/select', views.select_horse, name="select_horse"),

    path('horse/select2', views.select_horse2, name="select_horse2"),

    path('horse/<horse_pk>/edit', views.edit_horse, name="edit_horse"),

    path('combo-autocomplete', views.ComboAutocomplete.as_view(),
         name="combo_autocomplete"),

    path('division-autocomplete', views.DivisionAutocomplete.as_view(),
         name="division_autocomplete"),

    path('populate-pdf', views.populate_pdf, name="populate_pdf"),
]

urlpatterns = [
    path('', views.select_show, name="select_show"),

    path('add', views.add_show, name='add_show'),

    path('<show_date>/', include(show_patterns)),

    path('signup', views.sign_up, name='sign_up'),

    path('login', auth_views.LoginView.as_view(
        template_name='login.html'), name='log_in'),

    path('logout', auth_views.LogoutView.as_view(), name='log_out'),

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
# <<<<<<< HEAD
# =======
# urlpatterns = [
#     path('', views.show_select, name="show_select"),
#     path('signup', views.signup, name='signup'),
#     path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout', auth_views.LogoutView.as_view(), name='logout'),
#     path('create_show', views.create_show, name='create_show'),
#     path('showpage/<showdate>', views.showpage, name='showpage'),
#     path('<classname>/rankclass', views.rankclass, name='rankclass'),
#     path('horse/new', views.add_horse, name="add_horse"),
#     path('rider/new', views.add_rider, name="add_rider"),
#     path('class/new', views.new_class, name="classes"),
#     path('<showdate>/division/<divisionname>', views.division, name="division_info"),
#     path('<showdate>/<divisionname>/classes/<classnumber>', views.class_info, name="edit_class"),
#     path('<showdate>/<divisionname>/classes/<classnumber>/scratch/<combo>', views.delete_combo, name="delete_combo"),
#     path('<showdate>/newdivision', views.new_division, name="divisions"),
#     path('horse', views.select_horse, name="select_horse"),
#     path('class', views.class_select, name="class_select"),
#     path('<showdate>/division', views.division_select, name="division_select"),
#     path('<divisionname>/divisionscore', views.divisionscore, name="divisionscore"),
#     path('<divisionname>/division_classes', views.division_classes, name="division_classes"),
#     path('<showdate>/<divisionname>/<classnumber>/delete_class', views.delete_class, name="delete_class"),
#     path('<showdate>/billing', views.billing, name="billing"),
#     path('<showdate>/<combonum>/billinglist', views.billinglist, name="billinglist"),
#     path('<showdate>/<combonum>/scratch', views.scratch, name="scratch"),
#     path('show-autocomplete', views.ShowAutocomplete.as_view(), name="show_autocomplete"),
#     path('rider', views.select_rider, name="select_rider"),
#     path('select-rider', views.select_rider2, name="select_rider2"),
#     path('select-horse', views.select_horse2, name="select_horse2"),
#     path('rider-autocomplete', views.RiderAutocomplete.as_view(), name="rider_autocomplete"),
#     path('horse-autocomplete', views.HorseAutocomplete.as_view(), name="horse_autocomplete"),
#     path('class_autocomplete', views.ClassAutocomplete.as_view(), name="classes_autocomplete"),
#     path('combo_autocomplete', views.ComboAutocomplete.as_view(), name="combo_autocomplete"),
#     path('division_autocomplete', views.DivisionAutocomplete.as_view(), name="division_autocomplete"),
#     path('<showdate>/genpdf', views.populate_pdf, name="populate_pdf"),
#     path('add-combo', views.add_combo, name="add_combo"),
#     path('combo/<num>', views.edit_combo, name="edit_combo"),
#     path('rider/<rider_pk>', views.edit_rider, name="edit_rider"),
#     path('horse/<horse_pk>', views.edit_horse, name="edit_horse")
# ]
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# >>>>>>> 33eab3d2095c2aad5a11233b4d2c59e252f85505
