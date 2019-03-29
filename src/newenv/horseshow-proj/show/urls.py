from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

combo_patterns = [
    path('billing',
         views.view_billing, name="view_billing"),

    path('scratch', views.scratch_combo, name="scratch_combo"),

    path('edit', views.edit_combo, name="edit_combo"),
]

class_patterns = [
    path('',
         views.view_class, name="view_class"),

    path('rank',
         views.rank_class, name='rank_class'),

    path('delete',
         views.delete_class, name="delete_class"),

    path('combo/<combo_num>/', include(combo_patterns)),

    path('combo/<combo_num>/delete', views.delete_combo, name="delete_combo"),

]

division_patterns = [
    path('',
         views.view_division, name="view_division"),

    path('delete',
         views.delete_division, name="delete_division"),

    path('edit',
         views.edit_division, name="edit_division"),

    path('class/add',
         views.add_class, name="add_class"),

    path('class/select',
         views.select_class, name="select_class"),

    path('class/<class_num>/', include(class_patterns)),

    path('scores',
         views.view_division_scores, name="view_division_scores"),

    path('classes',
         views.view_division_classes, name="view_division_classes"),


]

rider_patterns = [
    # path('edit', views.edit_rider, name="edit_rider"),

    path('delete', views.delete_rider, name="delete_rider"),

    path('edit', views.update_rider, name="edit_rider"),


]

show_patterns = [
    path('view', views.view_show, name='view_show'),

    path('division/add', views.add_division, name="add_division"),

    path('division/select', views.select_division, name="select_division"),

    path('division/<division_id>/', include(division_patterns)),

    path('combo/add', views.add_combo, name="add_combo"),

    path('combo/select', views.select_combo, name="select_combo"),

    path('combo/<combo_num>/', include(combo_patterns)),

    path('horse/add', views.add_horse, name="add_horse"),

    path('horse/select', views.select_horse, name="select_horse"),

    path('horse/select2', views.select_horse2, name="select_horse2"),

    path('horse/<horse_pk>/edit', views.edit_horse, name="edit_horse"),

    path('populate-pdf', views.populate_pdf, name="populate_pdf"),
]

urlpatterns = [



    path('select', views.select_show, name="select_show"),


    path('all_riders', views.view_riders, name="view_riders"),

    path('get_rider_form/<rider_pk>',
         views.get_rider_form, name="get_rider_form_edit"),

    path('get_rider_form', views.get_rider_form, name="get_rider_form"),

    path('rider/<int:rider_pk>/', include(rider_patterns)),

    path('show-autocomplete', views.ShowAutocomplete.as_view(),
         name="show_autocomplete"),

    path('rider-autocomplete', views.RiderAutocomplete.as_view(),
         name="rider_autocomplete"),

    path('horse-autocomplete', views.HorseAutocomplete.as_view(),
         name="horse_autocomplete"),
    path('combo-autocomplete', views.ComboAutocomplete.as_view(),
         name="combo_autocomplete"),

    path('division-autocomplete', views.DivisionAutocomplete.as_view(),
         name="division_autocomplete"),
    path('class-autocomplete', views.ClassAutocomplete.as_view(),
         name="classes_autocomplete"),

    path('add-rider', views.update_rider, name="add_rider"),

    path('add', views.add_show, name='add_show'),

    path('<show_date>/', include(show_patterns)),


    path('signup', views.sign_up, name='sign_up'),

    path('login', auth_views.LoginView.as_view(
        template_name='log_in.html'), name='log_in'),

    path('logout', auth_views.LogoutView.as_view(), name='log_out'),

    path('<show_date>/generate_labels', views.generate_labels, name="labels"),



]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# old path('division/<division_id>/class<class_num>', include(class_patterns)),
