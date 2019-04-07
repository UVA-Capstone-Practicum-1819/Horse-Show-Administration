from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

combo_patterns = [
    path('view', views.view_combo, name="view_combo"),


    path('edit', views.edit_combo, name="edit_combo"),

    path('delete', views.delete_combo, name="delete_combo"),

    path('add-class', views.add_class_to_combo, name="add_class_to_combo"),

    path('delete-participation/<class_pk>', views.delete_participation,
         name="delete_participation")
]

class_patterns = [
    path('',
         views.view_class, name="view_class"),

    path('rank',
         views.rank_class, name='rank_class'),

    path('delete',
         views.delete_class, name="delete_class"),

    path('combo/<combo_pk>/', include(combo_patterns)),



]

participation_patterns = [
    path('get-class-in-combo-row', views.get_class_in_combo_row,
         name="get_class_in_combo_row")
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


    path('delete', views.delete_rider, name="delete_rider"),

    path('edit', views.update_rider, name="edit_rider"),


]

horse_patterns = [


    path('delete', views.delete_horse, name="delete_horse"),

    path('edit', views.update_horse, name="edit_horse"),


]

show_patterns = [
    path('view', views.view_show, name='view_show'),

    path('division/add', views.add_division, name="add_division"),

    path('division/select', views.select_division, name="select_division"),

    path('division/<division_id>/', include(division_patterns)),

    path('combo/add', views.add_combo, name="add_combo"),

    path('all_combos', views.view_combos, name="view_combos"),

    path('generate_labels', views.generate_labels, name="generate_labels"),

    path('populate-pdf', views.populate_pdf, name="populate_pdf"),

    path('populate-excel', views.populate_excel, name="populate_excel"),
]

urlpatterns = [

    path('select', views.select_show, name="select_show"),

    path('all_riders', views.view_riders, name="view_riders"),

    path('all_horses', views.view_horses, name="view_horses"),

    path('get_rider_form/<rider_pk>',
         views.get_rider_form, name="get_rider_form_edit"),

    path('get_combo_form/<combo_pk>',
         views.get_combo_form, name="get_combo_form_edit"),







    path('get_combo_form', views.get_combo_form, name="get_combo_form"),

    path('get_horse_form/<horse_pk>',
         views.get_horse_form, name="get_horse_form_edit"),

    path('get_rider_form', views.get_rider_form, name="get_rider_form"),

    path('get_horse_form', views.get_horse_form, name="get_horse_form"),

    path('combo/<combo_pk>/', include(combo_patterns)),



    path('rider/<int:rider_pk>/', include(rider_patterns)),



    path('horse/<int:horse_pk>/', include(horse_patterns)),


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

    path('add-horse', views.update_horse, name="add_horse"),

    path('add', views.add_show, name='add_show'),

    path('<show_date>/', include(show_patterns)),


    path('signup', views.sign_up, name='sign_up'),

    path('login', auth_views.LoginView.as_view(
        template_name='log_in.html'), name='log_in'),

    path('logout', auth_views.LogoutView.as_view(), name='log_out'),

    path('participations/<participation_pk>/', include(participation_patterns))



]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# old path('division/<division_id>/class<class_num>', include(class_patterns)),
