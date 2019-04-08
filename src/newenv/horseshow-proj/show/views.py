import random
import re
import os
import json
import pdfrw
import datetime
import io
from datetime import date
from django.http import FileResponse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import resolve, reverse
from show.forms import *
from django.contrib.auth import views as auth_views
from django.forms.models import model_to_dict
from django.db.models import Q
from show.models import *
from django.utils import timezone
from dal import autocomplete
from .populatepdf import write_fillable_pdf
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .labels import generate_show_labels
from xlutils.copy import copy
import xlrd
import xlwt
from operator import itemgetter


class AuthRequiredMiddleware(object):
    """
    Middleware required so that non-logged-in users cannot see pages they aren't authorized to see
    The exceptions are the login, signup, and admin pages
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        requested_path = request.path
        is_user_authenticated = request.user.is_authenticated

        # if the user is already authenticated, redirect user from login or signup to the index page, otherwise allow them to proceed as normal
        if re.match(r'/show/(login|signup)/?', requested_path):
            if not is_user_authenticated:
                return response
            else:
                return redirect('select_show')
        # if the user is not authenticated, redirect the user from any horseshow page to the login page
        if not is_user_authenticated:
            return redirect('log_in')

        return response


def view_show(request, show_date):
    """ used as the home page for a selected show """
    show = Show.objects.get(date=show_date)
    if request.method == "POST":
        form = ComboNumForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['num']
            combo = show.combos.filter(num=num)
            if combo:
                return redirect('edit_combo', combo_num=num, show_date=show_date)
            else:
                messages.error(request, "The combination number entered does not exist in this show.")
                return redirect('view_show', show_date=show_date)
    #for combo in HorseRiderCombo.objects.filter(show = show):
    #    if combo.num==num:
    #        return redirect('edit_combo', combo_num=num, show_date=show_date)
    #    else:
    #        print(combo.num)
    #        print(num)
    #        messages.error(request, "The combination number entered does not exist in this show.")
    #        return redirect('view_show', show_date=show_date)

    form = ComboNumForm()
    context = {
        "show_name": show.name,
        "date": show_date,
        "date_obj": datetime.datetime.strptime(show_date, "%Y-%m-%d"),
        "location": show.location,
        "divisions": show.divisions.all().order_by('first_class_num'),
        'form': form,

    }
    return render(request, 'view_show.html', context)


def add_show(request):
    """ view used to create the show, if successful, redirects to its show home page """
    form = ShowForm()
    if request.method == "POST":
        f = ShowForm(request.POST)
        if not f.is_valid():
            return render(request, 'add_show.html', {'form': f})
        show_name = f.cleaned_data['name']
        show_date = f.cleaned_data['date']
        if Show.objects.filter(date=show_date).count() == 1:
            response = {'ok': True, 'success_msg': "Cannot have Shows with same date",
                        'form': form}
            return render(request, 'add_show.html', response, {'form': f})
        show_location = f.cleaned_data['location']
        new_show = Show.objects.create(
            name=show_name, date=show_date, location=show_location,
            day_of_price=f.cleaned_data['day_of_price'], pre_reg_price=f.cleaned_data['pre_reg_price'])
        return redirect('view_show', show_date=show_date)
    else:
        return render(request, 'add_show.html', {'form': form})


def select_show(request):
    """ view that allows the user to select a show """
    context = {
        'shows': Show.objects.all()
    }

    return render(request, 'select_show.html', context)


def sign_up(request):  #pragma: no cover # what does this comment mean?
    """ creates a new user account """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('select_show')
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})


def select_combo(request, show_date):
    """ Used to retrieve information necessary for billing a rider """
    if request.method == "POST":
        form = ComboSelectForm(request.POST)
        # allows the user to select from the pre-existing horse-rider combos
        if form.is_valid():
            combo = form.cleaned_data['combo']
            return redirect('view_billing', show_date=show_date, combo_num=combo.num)
    else:
        form = ComboSelectForm()
    return render(request, 'select_combo.html', {'form': form, 'date': show_date})


def view_billing(request, show_date, combo_num):
    """ Billing list shows what horse rider combos need to be billed for and their total price based on
    whether or not they are pregistered for each class """
    show = Show.objects.get(date=show_date)
    combo = show.combos.filter(show=show_date).get(num=combo_num)
    participations = combo.participations.all()
    classes = combo.classes.all()
    total = classes.count()
    price = 0
    for classe in classes:
        class_pre_reg = ClassParticipation.objects.filter(
            combo=combo).get(participated_class=classe)
        if class_pre_reg.is_preregistered == True:
            price += show.pre_reg_price
        else:
            price += show.day_of_price
    #total = classes.count()
    #price = show.pre_reg_price * total
    # for minimum requirements, only calculates price based on pre-registration price
    context = {'name': combo.rider, 'show_date': show_date,
               'classes': participations, 'combo_num': combo_num, 'tot': total, 'price': price}
    # the context will help create the table for the list of classes a user is currently in
    return render(request, 'view_billing.html', context)


def scratch_combo(request, show_date, combo_num):
    """ This view allows you to scratch from a show """
    show = Show.objects.get(date=show_date)
    combo = show.combos.get(num=combo_num)
    class_num = request.GET["cnum"]
    class_obj = Class.objects.get(show=show, num=class_num)
    selected_class = ClassParticipation.objects.filter(
        combo=combo).get(participated_class=class_obj)
    selected_class.delete()
    return redirect('view_billing', show_date=show_date, combo_num=combo_num)
    # this line allows for a classes to be scratched (or removed) at no additional cost
    # the list will be changed based on what classes were removed
    # classes will only be removed from the horse-rider combo object, not from the entire database


def view_division_scores(request, show_date, division_id):
    """ displays list of classes in division, hrc winners of each of those classes from 1st-6th places, and form to enter champion info """

    # get the division from the show object
    show = Show.objects.get(date=show_date)
    division = show.divisions.get(id=division_id)

    form = DivisionChampForm()
    if request.method == "POST":
        form = DivisionChampForm(request.POST)
        if form.is_valid():
            champion = form.cleaned_data['champion']
            champion_pts = form.cleaned_data['champion_pts']
            champion_reserve = form.cleaned_data['champion_reserve']
            champion_reserve_pts = form.cleaned_data['champion_reserve_pts']
            # sets the division's champion field  equal to the value entered into the "champion" field of the DivisionChampForm
            division.champion = champion
            # sets the division's champion_pts field equal to the value entered into the "champion_pts" field of DivisionChampForm
            division.champion_pts = champion_pts
            # sets the division's champion_reserve field equal to the value entered into the "champion_reserve" field of DivisionChampForm
            division.champion_reserve = champion_reserve
            # sets the division's champion_reserve_pts field equal to the value entered into the "champion_reserve_pts" field of DivisionChampForm
            division.champion_reserve_pts = champion_reserve_pts
            division.save()  # saves the division object fields in the database

    else:
        form = DivisionChampForm()

    context = {'classes': division.classes.all(), 'date': show_date,
               'id': division_id, 'name': division.name, 'form': form}
    # passes the DivisionChampForm and the division's name and classes to "division_score.html" and renders that page
    return render(request, 'view_division_scores.html', context)


def delete_class(request, show_date, division_id, class_num):
    """ deletes a class from a division """
    show = Show.objects.get(date=show_date)
    division = show.divisions.get(id=division_id)
    class_obj = division.classes.get(num=class_num)
    # gets the division object from the division name that was passed in
    class_obj.delete()  # removes the class object
    if(len(division.classes.all())>0):
        division.first_class_num = division.classes.all()[0].num
        division.save()
    else:
        division.first_class_num = 1000
        division.save()
    # redirects to division_classes and passes in the division's name
    return redirect('view_division', show_date=show_date, division_id=division_id)

def delete_division(request, show_date, division_id):
    """deletes a division from a show"""
    show = Show.objects.get(date=show_date)
    """get division"""
    division = show.divisions.get(id=division_id)
    division.delete()
    """delete it"""
    return redirect('view_show', show_date=show_date)

def view_division_classes(request, show_date, division_id): #pragma: no cover
    """ lists the classes in a division """
    show = Show.objects.get(date=show_date)
    division = show.divisions.get(id=division_id)
    context = {'classes': division.classes.all(), 'id': division_id}
    # passes the division's name and classes to the "division_classes.html" and renders that page
    return render(request, 'view_division_classes.html', context)


def add_class(request, show_date, division_id):
    """ This view allows you to add a new class """
    show = Show.objects.get(date=show_date)
    division = show.divisions.get(id=division_id)
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            show = Show.objects.get(date=show_date)
            division = show.divisions.get(id=division_id)
            existing_classes = division.classes.filter(
                num=form.cleaned_data['num'])
            if existing_classes:
                messages.error(
                    request, 'Combo for selected horse and rider already exists!')
                return redirect('view_division_classes', show_date=show_date, division_id=division_id)
            class_form = ClassForm(request.POST)
            class_obj = class_form.save(commit=False)
            class_obj.division = division
            class_obj.show = show
            class_obj.save()
            return redirect('view_class', show_date=show_date, division_id=division_id, class_num=class_obj.num)
    else:
        form = ClassForm()
        context = {'name': division.name, 'form': form, 'date':show_date}
    return redirect('view_division', show_date=show_date, division_id=division_id) #goes to division page to add class


def select_class(request, show_date, division_id): #pragma: no cover
    """ This view allows you to select a class from a prepopulated list """
    if request.method == "POST":
        form = ClassSelectForm(request.POST)
        if form.is_valid():
            class_num = form.cleaned_data['num']
            request.session['class_obj'] = class_name
            return redirect('rank_class', show_date=show_date, division_id=division_id, class_num=class_num)
    else:
        form = ClassSelectForm()
    return render(request, 'select_class.html', {'form': form})


def rank_class(request, show_date, division_id, class_num):
    """
        This method ranks classes from 1st through 6th and stores the winning scores under
        specific horse rider combos that competed in that class and were awarded points
        points are always starting from 10, then 6, and so on
    """
    show = Show.objects.get(date=show_date)
    division = show.divisions.get(id=division_id)
    class_obj = division.classes.get(num=class_num)
    bool_error = False
    if request.method == 'POST':
        form = RankingForm(request.POST)
        if form.is_valid():

            rank_list = [form.cleaned_data['first'], form.cleaned_data['second'], form.cleaned_data['third'],
                         form.cleaned_data['fourth'], form.cleaned_data['fifth'], form.cleaned_data['sixth']]


            for i in rank_list:
                if i is None:
                    pass
                elif i < 100 or i > 999:
                    messages.error(request, "Invalid combination number " + str(
                        i) + ": combination number should be three digits: smallest 100, biggest 999")
                    bool_error = True
                elif show.combos.filter(num=i).count() == 0:
                    messages.error(request, "Cannot rank combination number " +
                                   str(i) + ": it is not registered to the show")
                    bool_error = True
            rank_list_without_none = [x for x in rank_list if x is not None]
            if len(set(rank_list_without_none)) != len(rank_list_without_none):

                messages.error(
                    request, "Same combination entered for more than one rank. Duplicates are not allowed in ranking.")

                bool_error = True
            if bool_error is True:
                # request.session['first'] = rank_list[0]
                # request.session['second'] = rank_list[1]
                # request.session['third'] = rank_list[2]
                # request.session['fourth'] = rank_list[3]
                # request.session['fifth'] = rank_list[4]
                # request.session['sixth'] = rank_list[5]
                # request.session['bool_error'] = True
                return redirect('rank_class', show_date=show_date, division_id=division_id, class_num=class_num)

            class_obj.first = rank_list[0]
            class_obj.second = rank_list[1]
            class_obj.third = rank_list[2]
            class_obj.fourth = rank_list[3]
            class_obj.fifth = rank_list[4]
            class_obj.sixth = rank_list[5]
            class_obj.save(
                update_fields=["first", "second", "third", "fourth", "fifth", "sixth"])

            combo_map = {
                form.cleaned_data['first']: 10,
                form.cleaned_data['second']: 6,
                form.cleaned_data['third']: 4,
                form.cleaned_data['fourth']: 2,
                form.cleaned_data['fifth']: 1,
                form.cleaned_data['sixth']: 0.5,
            }

            participations = class_obj.participations.all()

            for participation in participations:
                print(participation)
                combo_num = participation.combo.num
                if combo_num in combo_map:
                    participation.score = combo_map[combo_num]
                    participation.save(update_fields=["score"])

            return redirect('view_class', show_date=show_date, division_id=division_id, class_num=class_num)

    else:
        # print(bool_error)
        # if 'bool_error' in request.session:
        #     form = RankingForm(initial={'show_field': show_date, 'first': request.session['first'], 'second': request.session['second'], 'third': request.session['third'], 'fourth': request.session['fourth'], 'fifth': request.session['fifth'], 'sixth': request.session['sixth']})
        # else:
        form = RankingForm(initial={'first': class_obj.first, 'second': class_obj.second, 'third': class_obj.third,
                                    'fourth': class_obj.fourth, 'fifth': class_obj.fifth, 'sixth': class_obj.sixth})
        context = {
            "name": division.name,
            "class": class_obj,
            'form': form,
            'date':show_date
        }
        return render(request, 'rank_class.html', context)


def add_division(request, show_date):
    """ Form for allowing users to create a new division, which is a subset of show """
    show = Show.objects.get(date=show_date)

    if request.method == "POST":
        form = DivisionForm(request.POST)
        if form.is_valid():
            divisions = show.divisions.filter(name=form.cleaned_data['name'])
            if(len(divisions) > 0):
                # prepare error message, will display on submit.
                messages.error(
                    request, "The division name is in use. Please pick another division name.")
                return redirect('add_division', show_date=show_date)
            division_form = DivisionForm(request.POST)
            division = division_form.save(commit=False)
            division.show = show
            division.save()
            id = division.id
            print(id)
            return redirect('view_division', show_date=show_date, division_id=id)

    else:
        form = DivisionForm()

        context = {
            "form": form,
            "name": show.name,
            "date": show_date,
            "location": show.location,
            "divisions": show.divisions.all(),
        }
        return render(request, 'add_division.html', context)


def view_division(request, show_date, division_id):
    """ Info about divisions/classes in a show """
    show = Show.objects.get(date=show_date)
    division = show.divisions.get(id=division_id)
    if request.method == 'POST':  # if POST, create a new class for this division
        form = ClassForm(request.POST)
        if form.is_valid():
            # filter ALL show classes so that there are no duplicates across divisions
            existing_classes_count = Class.objects.filter(
                show=show, num=form.cleaned_data['num']).count()

            # verify number doesnt already exist
            if existing_classes_count > 0:
                # prepare error message, will display on submit.
                messages.error(request, "class number in use")
                return redirect('view_division', show_date=show_date, division_id=division_id)

            class_form = ClassForm(request.POST)
            class_obj = class_form.save(commit=False)
            class_obj.division = division
            class_obj.show = show
            class_obj.save()
            if(class_obj.num < division.first_class_num):
                division.first_class_num = int(class_obj.num)
                division.save()
            # render page with new division
            return redirect('view_division', show_date=show_date, division_id=division_id)
    else:
        division_classes = division.classes.all()
        form = ClassForm()
        context = {
            "date": show_date,
            "show_name": show.name,
            "id": division_id,
            "name": division.name,
            "classes": division_classes,
            "form": form,
        }
        return render(request, 'view_division.html', context)

def edit_division(request, show_date, division_id):
    """ view made for editing division name """
    show = Show.objects.get(date=show_date)
    division = show.divisions.get(id=division_id)
    if request.method == 'POST':  # if POST, save division's new name
        form = EditDivisionForm(request.POST)
        if form.is_valid():
            division.name = form.cleaned_data['change_name_to']
            division.save()
            # render page with new division
            return redirect('view_division', show_date=show_date, division_id=division_id)
    else:
        division_classes = division.classes.all()
        form = EditDivisionForm()
        context = {
            "date": show_date,
            "show_name": show.name,
            "id": division_id,
            "name": division.name,
            "classes": division_classes,
            "form": form,
        }
        return render(request, 'edit_division.html', context)


def view_class(request, show_date, division_id, class_num):
    """ render class info including combos in class """
    show = Show.objects.get(date=show_date)
    division = show.divisions.get(id=division_id)
    class_obj = division.classes.get(num=class_num)
    combos = class_obj.combos.all()
    if request.method == "POST":
        form = AddComboToClassForm(request.POST)
        # allows the user to enter a combo num they believe exists
        if form.is_valid():
            num = form.cleaned_data['num']
            # checking to see if combo number exists in this show
            try:
                combo = HorseRiderCombo.objects.get(show=show, num=num)
                # error checking for if combo is already in class
                combo_classes = combo.classes.all()
                if(class_obj in combo_classes):
                    messages.error(request, "Horse-Rider Combo is already in this class.")
                    return redirect('view_class', show_date=show_date, division_id=division_id, class_num=class_num)
                classParticipation = ClassParticipation(participated_class=class_obj, combo=combo, is_preregistered=form.cleaned_data['preregistered'])
                classParticipation.save()
                context = {
                    "combos": class_obj.combos.all(),
                    "class": class_obj,
                    "class_num": class_obj.num,
                    "date": show_date,
                    "id": division_id,
                    "name": division.name,
                    "show_name": show.name,
                    "add_form": form,
                }
                return render(request, 'view_class.html', context)
            except:
                messages.error(request, "Horse Rider Combo does not exist in this show.")
                return redirect('view_class', show_date=show_date, division_id=division_id, class_num=class_num)
    else:
        form = AddComboToClassForm(initial={'is_preregistered':True})
    # form = ComboSelectForm()
    context = {
        "combos": combos,
        "class": class_obj,
        "class_num": class_obj.num,
        "date": show_date,
        "id": division_id,
        "name": division.name,
        "show_name": show.name,
        "add_form": form,
    }
    return render(request, "view_class.html", context)  # render info


def delete_combo(request, show_date, division_id, class_num, combo_num):
    """ scratch a combo from the class page so that it reflects in the combo's billing """
    combo = HorseRiderCombo.objects.get(num=combo_num)
    show = Show.objects.get(date=show_date)
    division = show.divisions.get(id=division_id)
    class_obj = division.classes.get(num=class_num)
    selected_class = ClassParticipation.objects.filter(
        combo=combo).get(participated_class=class_obj)
    selected_class.delete()
    return redirect('view_class', show_date=show_date, division_id=division_id, class_num=class_num)


def select_division(request, show_date): #pragma: no cover
    """ displays division select dropdown and ability to "Save" or "See Division Scores" """
    if request.method == "POST":

        if 'save' in request.POST:  # if a division is selected and the "Save" button is clicked
            form = DivisionSelectForm(request.POST)
            if form.is_valid():
                show = Show.objects.get(date=show_date)
                return redirect('view_division_classes', show_date=show_date, division_id=form.cleaned_data['division'])
        if 'score' in request.POST:  # if a division is selected and the "See Divison Scores" button is clicked
            form = DivisionSelectForm(request.POST)
            if form.is_valid():
                division_obj = form.cleaned_data['division']
                divisions = Division.objects.all()
                for division in divisions:
                    if division_obj == division:
                        # redirects to divisionscore and passes in the division_name
                        return redirect('view_division_scores', show_date=show_date, division_id=division.id)

    else:
        form = DivisionSelectForm()
    return render(request, 'select_division.html', {'form': form, 'date': show_date})


def select_rider(request, show_date):
    """ selects a rider from a dropdown and stores its primary key into a session """
    if request.method == "POST":
        request.session['rider_pk'] = request.POST['rider']
        return redirect('select_horse', show_date=show_date)
    form = RiderSelectForm()
    return render(request, 'select_rider.html', {'form': form, 'date': show_date})


def select_rider2(request, show_date):
    """ select rider function exclusively for editing a rider """
    if request.method == "POST":
        rider_pk = request.POST['rider']
        return redirect('edit_rider', rider_pk=rider_pk, show_date=show_date)
    form = RiderSelectForm()
    return render(request, 'select_rider2.html', {'form': form, 'date': show_date})


def edit_rider(request, show_date, rider_pk):
    """ allows user to change the given fields in rider and save changes """
    rider = Rider.objects.get(pk=rider_pk)
    if request.method == "POST":
        edit_form = RiderEditForm(request.POST)
        if edit_form.is_valid():
            rider.first_name = edit_form.cleaned_data['first_name']
            rider.last_name = edit_form.cleaned_data['last_name']
            rider.address = edit_form.cleaned_data['address']
            rider.city = edit_form.cleaned_data['city']
            rider.state = edit_form.cleaned_data['state']
            rider.zip_code = edit_form.cleaned_data['zip_code']
            rider.birth_date = edit_form.cleaned_data['birth_date']
            rider.member_VHSA = edit_form.cleaned_data['member_VHSA']
            rider.member_4H = edit_form.cleaned_data['member_4H']
            rider.county = edit_form.cleaned_data['county']
            rider.save()
    else:
        edit_form = RiderEditForm(
            {'first_name': rider.first_name, 'last_name': rider.last_name, 'address': rider.address, 'city': rider.city, 'state': rider.state, 'zip_code': rider.zip_code,
             'birth_date': rider.birth_date, 'member_VHSA': rider.member_VHSA, 'member_4H': rider.member_4H, 'county': rider.county},
            instance=rider)
    return render(request, 'edit_rider.html', {'rider': rider, 'edit_rider_form': edit_form, 'date': show_date})


def add_rider(request, show_date):
    """ creates a new rider in a form and stores its primary key into a session, then redirects to select_horse """
    if request.method == "POST":
        form = RiderForm(request.POST)
        if form.is_valid():
            rider = form.save()
            request.session['rider_pk'] = rider.pk
            return redirect('select_horse', show_date=show_date)
    form = RiderForm()
    return render(request, 'add_rider.html', {'form': form, 'date': show_date})


def select_horse2(request, show_date):
    """ select horse function exclusively for editing a horse """
    if request.method == "POST":
        horse_pk = request.POST['horse']
        return redirect('edit_horse', horse_pk=horse_pk, show_date=show_date)
    form = HorseSelectForm()
    return render(request, 'select_horse2.html', {'form': form, 'date': show_date})


def edit_horse(request, horse_pk, show_date):
    """ allows user to change the given fields in rider and save changes """
    horse = Horse.objects.get(pk=horse_pk)
    if request.method == "POST":
        edit_form = HorseEditForm(request.POST)
        if edit_form.is_valid():
            horse.accession_num = edit_form.cleaned_data['accession_num']
            horse.coggins_date = edit_form.cleaned_data['coggins_date']
            horse.owner = edit_form.cleaned_data['owner']
            horse.type = edit_form.cleaned_data['type']
            horse.size = edit_form.cleaned_data['size']
            horse.save()

    edit_horse_form = HorseEditForm(
        {'accession_num': horse.accession_num, 'coggins_date': horse.coggins_date,
         'owner': horse.owner, 'type': horse.type, 'size': horse.size},
        instance=horse)
    return render(request, 'edit_horse.html', {'horse': horse, 'edit_horse_form': edit_horse_form, 'date': show_date})


def add_horse(request, show_date):
    """ creates a new horse in a form and stores its primary key into a session, then redirects to add_combo """
    if request.method == "POST":
        form = HorseForm(request.POST)
        if form.is_valid():
            horse = form.save()
            request.session['horse_pk'] = horse.pk
            return redirect('add_combo', show_date=show_date)
    form = HorseForm()
    return render(request, 'add_horse.html', {'form': form, 'date': show_date})


def select_horse(request, show_date):
    """ selects a horse from a dropdown and stores its primary key into a session """
    if request.method == 'POST':
        horse = request.POST['horse']
        request.session['horse_pk'] = request.POST['horse']
        return redirect('add_combo', show_date=show_date)
    form = HorseSelectForm()
    return render(request, 'select_horse.html', {'form': form, 'date': show_date})


def add_combo(request, show_date): #pragma: no cover
    """
        creates a page for adding a horse-rider combination, taking in the session variables for the primary keys of the chosen horse and rider
        redirects to the edit combo page for the same combination after it is done
     """
    show = Show.objects.get(date=show_date)
    form_errors = ""
    if request.method == 'POST':
        form = HorseRiderComboCreateForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['num']
            email = form.cleaned_data['email']
            cell = form.cleaned_data['cell']
            contact = form.cleaned_data['contact']
            rider_pk = request.session['rider_pk']
            horse_pk = request.session['horse_pk']
            rider = get_object_or_404(Rider, pk=rider_pk)
            horse = get_object_or_404(Horse, pk=horse_pk)
            try:
                HorseRiderCombo.objects.create(num=num, rider=rider, horse=horse,
                                               cell=cell, email=email, show=show)
            except IntegrityError:
                #messages.error(request, "HRC already exists!")
                messages.info(
                    request, 'Combo for selected horse and rider already exists!')
                return redirect('select_rider', show_date=show.date)
            return redirect('edit_combo', show_date=show.date, combo_num=num)
        else:
            form_errors = form.non_field_errors
    rider_pk = request.session['rider_pk']
    if rider_pk is None:
        return redirect('select_show')
    horse_pk = request.session['horse_pk']
    if horse_pk is None:
        return redirect('select_show')
    rider = get_object_or_404(Rider, pk=rider_pk)
    horse = get_object_or_404(Horse, pk=horse_pk)
    form = HorseRiderComboCreateForm()

    return render(request, 'add_combo.html', {'form': form,  'rider': rider, 'horse': horse, 'date': show_date, 'form_errors': form_errors})


def edit_combo(request, show_date, combo_num, division_id=None, class_num=None): #pragma: no cover
    """
    edits the combination that was specified by num
    also handles the addition/removal of classes based on num and the calculation of price
     """
    show = Show.objects.get(date=show_date)
    combo = show.combos.get(num=combo_num)
    # edit_form = HorseRiderEditForm(
    #     {'email': combo.email, 'cell': combo.cell, 'contact': combo.contact}, instance=combo)

    # class_combo_form = ClassComboForm()

    # registered_classes = combo.classes.all()
    # number_registered_classes = len(registered_classes)
    # price = number_registered_classes * 10
    # participations = combo.participations.all()
    # # print(participations)
    # for participation in participations:
    #     if participation.is_preregistered:
    #         price += show.pre_reg_price
    #     else:
    #         price += show.day_of_price
    if request.method == "POST":
        if request.POST.get('remove_class'):
            num = request.POST['remove_class']
            class_obj = Class.objects.filter(show=show_date).get(num=num)
            selected_class = ClassParticipation.objects.filter(
                combo=combo).get(participated_class=class_obj)
            selected_class.delete()

        if request.POST.get('add_class'):
            class_combo_form = ClassComboForm(request.POST)

            if class_combo_form.is_valid():
                selected_class = class_combo_form.cleaned_data['num']
                is_prereg = class_combo_form.cleaned_data['is_preregistered']
                try: #checks to see if class creation is valid
                    class_obj = Class.objects.filter(show=show_date).get(num=selected_class)
                    classParticipation = ClassParticipation(
                    participated_class=class_obj, combo=combo, is_preregistered=is_prereg)
                    try:
                        classParticipation.save()
                    except IntegrityError: #if combo already in class, show error on edit combo page
                        messages.info(request, "Combo is already registered for class "+str(class_combo_form.cleaned_data['num']))
                except ObjectDoesNotExist:
                    messages.error(request, "The class number entered does not exist in this show.")
        elif request.POST.get('edit'):
            edit_form = HorseRiderEditForm(request.POST)

            if edit_form.is_valid():
                combo.email = edit_form.cleaned_data['email']
                combo.cell = edit_form.cleaned_data['cell']
                combo.contact = edit_form.cleaned_data['contact']
                combo.save()
    edit_form = HorseRiderEditForm(
        {'email': combo.email, 'cell': combo.cell, 'contact': combo.contact}, instance=combo)

    class_combo_form = ClassComboForm(initial={'is_preregistered':True})
    registered_classes = combo.classes.all()
    number_registered_classes = len(registered_classes)
    price = 0
    participations = combo.participations.all()
    for participation in participations:
        if participation.is_preregistered:
            price += show.pre_reg_price
        else:
            price += show.day_of_price
    if division_id != None:
        division = Division.objects.get(id=division_id)
        c = Class.objects.get(show=show, num=class_num)
        return render(request, 'edit_combo.html', {'division':division, 'class':c, 'show':show, 'combo': combo, 'edit_form': edit_form,
            'class_combo_form': class_combo_form, 'classes': participations, 'date': show_date})
    else:
        return render(request, 'edit_combo.html', {'combo': combo, 'edit_form': edit_form, 'class_combo_form': class_combo_form,
            'classes': participations, 'date': show_date})


class ShowAutocomplete(autocomplete.Select2QuerySetView):  #pragma: no cover
    """ Autocomplete functionality for the select page """

    def get_queryset(self):
        # if not self.request.user.is_authenticated():
            # return Horse.objects.none()
        qs = Show.objects.all().order_by('date')
        if self.q:
            qs = qs.filter(show_name__istartswith=self.q)
        return qs


class ComboAutocomplete(autocomplete.Select2QuerySetView):  #pragma: no cover
    """ Autocomplete functionality for selecting a combo """

    def get_queryset(self):
        qs = HorseRiderCombo.objects.all().order_by('num')
        if self.q:
            qs = qs.filter(class_name__istartswith=self.q)
        return qs


class ClassAutocomplete(autocomplete.Select2QuerySetView):  #pragma: no cover
    """ This is the autocomplete functionality for selecting a class """

    def get_queryset(self):
        qs = Class.objects.all().order_by('num')
        if self.q:
            qs = qs.filter(class_name__istartswith=self.q)
        return qs


class RiderAutocomplete(autocomplete.Select2QuerySetView):  #pragma: no cover
    """ This view shows the autocomplete functionality for selection a rider """

    def get_queryset(self):
        qs = Rider.objects.all().order_by('last_name')
        if self.q:
            qs = qs.filter(Q(last_name__istartswith=self.q) | Q(first_name__istartswith=self.q))
        return qs


class HorseAutocomplete(autocomplete.Select2QuerySetView):  #pragma: no cover
    """ This view shows the autocomplete functionality for selecting a horse """

    def get_queryset(self):
        # orders horses in dropdown queryset by name
        qs = Horse.objects.all().order_by('name')

        if self.q:
            # filters horses in dropdown queryset by checking if horses' names start with the text entered into the field
            qs = qs.filter(name__istartswith=self.q)

        return qs


class DivisionAutocomplete(autocomplete.Select2QuerySetView):  #pragma: no cover
    """ fills in form automatically based on value entered by user """

    def get_queryset(self):
        qs = Division.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(division_name__istartswith=self.q)
        return qs


def populate_pdf_division(division_name, page, show, d):  #pragma: no cover
    for division in Division.objects.filter(name__icontains=division_name):
        if division.show.date == show.date:
            # print(division.name)
            dp = "p" + str(page)
            d[dp + "_show_name"] = show.name
            d[dp + "_show_date"] = show.date
            int = 1
            for c in Class.objects.filter(division__name__icontains=division_name):
                if c.show.date == show.date:
                    # print(c.num)
                    # set the key to the right class (initially c1) text field
                    s = dp + '_c' + str(int)
                    d[s] = c.num  # add to the dictionary the class number
                    # set the key to the right entry (initially c1) text field
                    e = dp + '_e' + str(int)
                    num_entry = ClassParticipation.objects.filter(
                        participated_class=c).count()
                    d[e] = num_entry
                    # for combo in HorseRiderCombo.objects.filter(classes__num=c.num):
                    # print(combo.horse.name)
                    # print(combo.rider.name)
                    # print(combo.horse.owner)
                    # create a list that stores rank 1-6 in that class
                    list = (c.first, c.second, c.third,
                            c.fourth, c.fifth, c.sixth)
                    for i in range(1, 7):  # for i range from 1st place to 6th place
                        # set the keys to the right combo, owner and rider text fields
                        shorse = s + '_combo' + str(i)
                        sowner = s + '_owner' + str(i)
                        srider = s + '_rider' + str(i)
                        # if the class is already ranked, and there exist a combo associate with the rank
                        if list[i-1] != 0:
                            try:  # get the combo that is placed at each rank, write to pdf the rider and horse owner associated with combo
                                combo = HorseRiderCombo.objects.get(
                                    num=list[i-1])
                                # write to pdf the correct combo to that rank
                                d[shorse] = combo.horse
                                d[srider] = combo.rider.first_name + combo.rider.last_name
                                d[sowner] = combo.horse.owner
                            except ObjectDoesNotExist:
                                print("")
                int += 1
            d[dp + "_champ"] = division.champion
            d[dp + "_rchamp"] = division.champion_reserve


def populate_pdf_division_combine_by_age(division_name, page1, page2, show, d, bool_combine):  #pragma: no cover
    for division in Division.objects.filter(name__icontains=division_name):
        # combined = True;
        # div2 = Division.objects.filter(name__icontains=division_name2).filter(name__icontains="hunter")
        # if div2.count()>0:
        #     if div2.show.date == show.date:
        #     #check num entry combined > 2
        #         for c in Class.objects.filter(division__name__icontains=division_name2).filter(division__name__icontains="hunter"):
        #             if c.show.date == show.date:
        #                 num_entry = ClassParticipation.objects.filter(participated_class=c).count()
        #                 if num_entry > 2:
        #                     combined = False;

        if division.show.date == show.date:
            # print(division.name)
            dp = "p" + str(page1)
            dp2 = "p" + str(page2)
            d[dp + "_show_name"] = show.name
            d[dp + "_show_date"] = show.date
            int = 1
            for c in Class.objects.filter(division__name__icontains=division_name):
                if c.show.date == show.date:
                    # set the key to the right class (initially c1) text field
                    s = dp + '_c' + str(int)
                    d[s] = c.num  # add to the dictionary the class number
                    # set the key to the right entry (initially c1) text field
                    e = dp + '_e' + str(int)
                    num_entry = ClassParticipation.objects.filter(
                        participated_class=c).count()
                    d[e] = num_entry
                    # create a list that stores rank 1-6 in that class
                    list = (c.first, c.second, c.third,
                            c.fourth, c.fifth, c.sixth)
                    for i in range(1, 7):  # for i range from 1st place to 6th place
                        # set the keys to the right combo, owner and rider text fields
                        shorse = s + '_combo' + str(i)
                        sowner = s + '_owner' + str(i)
                        srider = s + '_rider' + str(i)
                        # if the class is already ranked, and there exist a combo associate with the rank
                        if list[i-1] != 0:
                            try:  # get the combo that is placed at each rank, write to pdf the rider and horse owner associated with combo
                                combo = HorseRiderCombo.objects.get(
                                    num=list[i-1])
                                if combo.rider.adult is False:
                                    # write to pdf the correct combo to that rank
                                    d[shorse] = combo.horse
                                    d[srider] = combo.rider.first_name + combo.rider.last_name
                                    d[sowner] = combo.horse.owner
                                else:
                                    bool_combine = True

                                    d[dp2 + '_c' + str(int) + '_combo' + str(i)] = combo.horse # write to pdf the correct combo to that rank
                                    d[dp2 + '_c' + str(int) + '_rider' + str(i)] = combo.rider.first_name + combo.rider.last_name
                                    d[dp2 + '_c' + str(int) + '_owner' + str(i)] = combo.horse.owner


                            except ObjectDoesNotExist:
                                print("")
                    if bool_combine is True:
                        # print(c.num)
                        d[dp2 + "_show_name"] = show.name
                        d[dp2 + "_show_date"] = show.date
                        # set the key to the right class (initially c1) text field
                        s = dp2 + '_c' + str(int)
                        d[s] = c.num  # add to the dictionary the class number
                        # set the key to the right entry (initially c1) text field
                        e = dp2 + '_e' + str(int)
                        num_entry = ClassParticipation.objects.filter(
                            participated_class=c).count()
                        d[e] = num_entry
                int += 1
            d[dp + "_champ"] = division.champion
            d[dp2 + "_champ"] = division.champion
            d[dp + "_rchamp"] = division.champion_reserve
            d[dp2 + "_rchamp"] = division.champion_reserve
    return bool_combine


def populate_pdf_division_combine_by_hsize(division_name, page2, page1, show, d, bool_combine):  #pragma: no cover
    for division in Division.objects.filter(name__icontains=division_name):
        if division.show.date == show.date:
            # print(division.name)
            dp = "p" + str(page1)
            dp2 = "p" + str(page2)
            d[dp + "_show_name"] = show.name
            d[dp + "_show_date"] = show.date
            int = 1
            for c in Class.objects.filter(division__name__icontains=division_name):
                if c.show.date == show.date:
                    # set the key to the right class (initially c1) text field
                    s = dp + '_c' + str(int)
                    d[s] = c.num  # add to the dictionary the class number
                    # set the key to the right entry (initially c1) text field
                    e = dp + '_e' + str(int)
                    num_entry = ClassParticipation.objects.filter(
                        participated_class=c).count()
                    d[e] = num_entry
                    # for combo in HorseRiderCombo.objects.filter(classes__num=c.num):
                    # create a list that stores rank 1-6 in that class
                    list = (c.first, c.second, c.third,
                            c.fourth, c.fifth, c.sixth)
                    for i in range(1, 7):  # for i range from 1st place to 6th place
                        # set the keys to the right combo, owner and rider text fields
                        shorse = s + '_combo' + str(i)
                        sowner = s + '_owner' + str(i)
                        srider = s + '_rider' + str(i)
                        # if the class is already ranked, and there exist a combo associate with the rank
                        if list[i-1] != 0:
                            try:  # get the combo that is placed at each rank, write to pdf the rider and horse owner associated with combo
                                combo = HorseRiderCombo.objects.get(
                                    num=list[i-1])
                                print(combo.horse.size)
                                if combo.horse.type == "pony":
                                    if combo.horse.size == "large":
                                        # write to pdf the correct combo to that rank
                                        d[shorse] = combo.horse
                                        d[srider] = combo.rider.first_name + combo.rider.last_name
                                        d[sowner] = combo.horse.owner
                                    elif combo.horse.size == "medium" or combo.horse.size == "small":
                                        bool_combine = True
                                        # write to pdf the correct combo to that rank
                                        d[dp2 + '_c' +
                                            str(int) + '_combo' + str(i)] = combo.horse
                                        d[dp2 + '_c' + str(int) + '_rider' +
                                          str(i)] = combo.rider.first_name + combo.rider.last_name
                                        d[dp2 + '_c' + str(int) + '_owner' +
                                          str(i)] = combo.horse.owner
                            except ObjectDoesNotExist:
                                print("")
                    if bool_combine is True:
                        # print(c.num)
                        d[dp2 + "_show_name"] = show.name
                        d[dp2 + "_show_date"] = show.date
                        # set the key to the right class (initially c1) text field
                        s = dp2 + '_c' + str(int)
                        d[s] = c.num  # add to the dictionary the class number
                        # set the key to the right entry (initially c1) text field
                        e = dp2 + '_e' + str(int)
                        num_entry = ClassParticipation.objects.filter(
                            participated_class=c).count()
                        d[e] = num_entry
                int += 1
            d[dp + "_champ"] = division.champion
            d[dp2 + "_champ"] = division.champion
            d[dp + "_rchamp"] = division.champion_reserve
            d[dp2 + "_rchamp"] = division.champion_reserve
    return bool_combine


def populate_pdf_division_combine_by_htype(division_name, page1, page2, show, d, bool_combine):  #pragma: no cover
    for division in Division.objects.filter(name__icontains=division_name):
        if division.show.date == show.date:
            # print(division.name)
            dp = "p" + str(page1)
            dp2 = "p" + str(page2)
            d[dp + "_show_name"] = show.name
            d[dp + "_show_date"] = show.date
            int = 1
            for c in Class.objects.filter(division__name__icontains=division_name):
                if c.show.date == show.date:
                    # set the key to the right class (initially c1) text field
                    s = dp + '_c' + str(int)
                    d[s] = c.num  # add to the dictionary the class number
                    # set the key to the right entry (initially c1) text field
                    e = dp + '_e' + str(int)
                    num_entry = ClassParticipation.objects.filter(
                        participated_class=c).count()
                    d[e] = num_entry
                    # for combo in HorseRiderCombo.objects.filter(classes__num=c.num):
                    # create a list that stores rank 1-6 in that class
                    list = (c.first, c.second, c.third,
                            c.fourth, c.fifth, c.sixth)
                    for i in range(1, 7):  # for i range from 1st place to 6th place
                        # set the keys to the right combo, owner and rider text fields
                        shorse = s + '_combo' + str(i)
                        sowner = s + '_owner' + str(i)
                        srider = s + '_rider' + str(i)
                        # if the class is already ranked, and there exist a combo associate with the rank
                        if list[i-1] != 0:
                            try:  # get the combo that is placed at each rank, write to pdf the rider and horse owner associated with combo
                                combo = HorseRiderCombo.objects.get(
                                    num=list[i-1])
                                print(combo.horse.type)
                                if combo.horse.type == "pony":
                                    # write to pdf the correct combo to that rank
                                    d[shorse] = combo.horse
                                    d[srider] = combo.rider.first_name + combo.rider.last_name
                                    d[sowner] = combo.horse.owner
                                else:
                                    bool_combine = True
                                    # write to pdf the correct combo to that rank
                                    d[dp2 + '_c' +
                                        str(int) + '_combo' + str(i)] = combo.horse
                                    d[dp2 + '_c' + str(int) + '_rider' +
                                      str(i)] = combo.rider.first_name + combo.rider.last_name
                                    d[dp2 + '_c' + str(int) + '_owner' +
                                      str(i)] = combo.horse.owner
                            except ObjectDoesNotExist:
                                print("")
                    if bool_combine is True:
                        # print(c.num)
                        d[dp2 + "_show_name"] = show.name
                        d[dp2 + "_show_date"] = show.date
                        # set the key to the right class (initially c1) text field
                        s = dp2 + '_c' + str(int)
                        d[s] = c.num  # add to the dictionary the class number
                        # set the key to the right entry (initially c1) text field
                        e = dp2 + '_e' + str(int)
                        num_entry = ClassParticipation.objects.filter(
                            participated_class=c).count()
                        d[e] = num_entry
                int += 1
            d[dp + "_champ"] = division.champion
            d[dp2 + "_champ"] = division.champion
            d[dp + "_rchamp"] = division.champion_reserve
            d[dp2 + "_rchamp"] = division.champion_reserve
    return bool_combine


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def populate_pdf(request, show_date): #pragma: no cover
    """ populate pdf for VHSA horse show reports """ #populates text fields of PDF
    show = Show.objects.get(date=show_date)  # get the show by its date
    d = {
        'p2_show_name': show.name,
        'p2_show_date': show_date,
    }  # populate the 2nd page of pdf with the show name and show time.
    p3_combine = False
    p5_combine = False
    p7_combine = False

    # p3 Junior/Children's Hunter
    # p4 Amateur Hunter
    try:

        p3_combine = populate_pdf_division_combine_by_age("Amateur", 3, 4, show, d, p3_combine)
    except ObjectDoesNotExist:
        print("")

    #p5 Small/Medium Pony Hunter
    #p6 Large Pony Hunter
    try:
        p5_combine = populate_pdf_division_combine_by_hsize("Pony Hunter", 5, 6, show, d, p5_combine)

    except ObjectDoesNotExist:
        print("")

    # p7 green hunter pony
    # p8 green hunter horse
    try:

        p7_combine = populate_pdf_division_combine_by_htype("Green Hunter", 7, 8, show, d, p7_combine)

    except ObjectDoesNotExist:
        print("")

    try:  # p9 Thoroughbred Hunter
        populate_pdf_division("Thoroughbred Hunter", 9, show, d)
    except ObjectDoesNotExist:
        print("")


    try: # p10 working Hunter

        populate_pdf_division("Working", 10, show, d)
    except ObjectDoesNotExist:
        print("")


    try: #p11 Hunter Pleasure Pony

        populate_pdf_division("Hunter Pleasure Pony", 11, show, d)
    except ObjectDoesNotExist:
        print("")

    try:  # p12 Junior Hunter Pleasure Horse
        populate_pdf_division("Junior Hunter Pleasure", 12, show, d)
    except ObjectDoesNotExist:
        print("")

    try:  # p13 Adult Hunter Pleasure Horse
        populate_pdf_division("Adult Hunter Pleasure", 13, show, d)
    except ObjectDoesNotExist:
        print("")

    try:  # p14 Hunter Short Stirrup
        populate_pdf_division("Short Stirrup", 14, show, d)
    except ObjectDoesNotExist:
        print("")

    # p15 Associate Equitation Classes (adult/children/pony)
    for division in Division.objects.filter(name__icontains="Equitation").exclude(name__icontains="Flat"):
        if division.show.date == show.date:
            dp = "p15"
            d[dp + "_show_name"] = show.name
            d[dp + "_show_date"] = show.date
            for c in Class.objects.filter(division__name__icontains="Equitation").exclude(division__name__icontains="Flat").filter(division__name__icontains="Adult"):
                if c.show.date == show.date:
                    fill_class_num_adult = False
                    fill_class_num_child = False
                    # create a list that stores rank 1-6 in that class
                    list = (c.first, c.second, c.third,
                            c.fourth, c.fifth, c.sixth)
                    for i in range(1, 7):  # for i range from 1st place to 6th place
                        # set the keys to the right combo, owner and rider text fields
                        # if the class is already ranked, and there exist a combo associate with the rank
                        if list[i-1] != 0:
                            try:  # get the combo that is placed at each rank, write to pdf the rider and horse owner associated with combo
                                combo = HorseRiderCombo.objects.get(
                                    num=list[i-1])
                                if combo.rider.adult is True and combo.horse.type == "horse":
                                    fill_class_num_adult = True
                                    d[dp + '_c' + str(1) + '_combo' +
                                      str(i)] = combo.rider.first_name + combo.rider.last_name
                                if combo.rider.adult is False and combo.horse.type == "horse":
                                    fill_class_num_child = True
                                    d[dp + '_c' + str(2) + '_combo' +
                                      str(i)] = combo.rider.first_name + combo.rider.last_name
                            except ObjectDoesNotExist:
                                print("")
                    if fill_class_num_adult is True:
                        d[dp + '_c' + str(1)] = c.num
                        e = dp + '_e' + str(1)
                        num_entry = ClassParticipation.objects.filter(
                            participated_class=c).count()
                        d[e] = num_entry
                    if fill_class_num_child is True:
                        d[dp + '_c' + str(2)] = c.num
                        e = dp + '_e' + str(2)
                        num_entry = ClassParticipation.objects.filter(
                            participated_class=c).count()
                        d[e] = num_entry
            for c in Class.objects.filter(division__name__icontains="Equitation").exclude(division__name__icontains="Flat").filter(division__name__icontains="Pony"):
                if c.show.date == show.date:
                    fill_class_num_pony = False
                    # create a list that stores rank 1-6 in that class
                    list = (c.first, c.second, c.third,
                            c.fourth, c.fifth, c.sixth)
                    for i in range(1, 7):  # for i range from 1st place to 6th place
                        # if the class is already ranked, and there exist a combo associate with the rank
                        if list[i-1] != 0:
                            try:  # get the combo that is placed at each rank, write to pdf the rider and horse owner associated with combo
                                combo = HorseRiderCombo.objects.get(
                                    num=list[i-1])
                                print(combo.horse.type)
                                if combo.horse.type == "pony":
                                    fill_class_num_pony = True
                                    d[dp + '_c' + str(3) + '_combo' +
                                      str(i)] = combo.rider.first_name + combo.rider.last_name
                            except ObjectDoesNotExist:
                                print("")
                    if fill_class_num_pony is True:
                        d[dp + '_c' + str(3)] = c.num
                        e = dp + '_e' + str(3)
                        num_entry = ClassParticipation.objects.filter(
                            participated_class=c).count()
                        d[e] = num_entry
            d[dp + "_champ"] = division.champion
            d[dp + "_rchamp"] = division.champion_reserve

    #p16 Associate Equitation On the Flat Classes (adult/children)
    for division in Division.objects.filter(name__icontains="Flat"):
        if division.show.date == show.date:
            dp = "p16"
            d[dp + "_show_name"] = show.name
            d[dp + "_show_date"] = show.date
            for c in Class.objects.filter(division__name__icontains="Flat").filter(division__name__icontains="Adult"):
                if c.show.date == show.date:
                    fill_class_num_adult = False
                    fill_class_num_child_15_17 = False
                    fill_class_num_child_14_less = False
                    # create a list that stores rank 1-6 in that class
                    list = (c.first, c.second, c.third,
                            c.fourth, c.fifth, c.sixth)
                    for i in range(1, 7):  # for i range from 1st place to 6th place
                        # set the keys to the right combo, owner and rider text fields
                        # if the class is already ranked, and there exist a combo associate with the rank
                        if list[i-1] != 0:
                            try:  # get the combo that is placed at each rank, write to pdf the rider and horse owner associated with combo
                                combo = HorseRiderCombo.objects.get(
                                    num=list[i-1])
                                if combo.rider.adult is True and combo.horse.type == "horse":
                                    fill_class_num_adult = True
                                    d[dp + '_c' + str(1) + '_combo' +
                                      str(i)] = combo.rider.first_name + combo.rider.last_name
                                if combo.rider.adult is False:
                                    age = calculate_age(combo.rider.birth_date)
                                    if 15 <= age <= 17:
                                        fill_class_num_child_15_17 = True
                                        d[dp + '_c' + str(2) + '_combo' +
                                          str(i)] = combo.rider.first_name + combo.rider.last_name
                                    if age <= 14:
                                        fill_class_num_child_14_less = True
                                        d[dp + '_c' + str(3) + '_combo' +
                                          str(i)] = combo.rider.first_name + combo.rider.last_name
                            except ObjectDoesNotExist:
                                print("")
                    if fill_class_num_adult is True:
                        d[dp + '_c' + str(1)] = c.num
                        e = dp + '_e' + str(1)
                        num_entry = ClassParticipation.objects.filter(
                            participated_class=c).count()
                        d[e] = num_entry
                    if fill_class_num_child_15_17 is True:
                        d[dp + '_c' + str(2)] = c.num
                        e = dp + '_e' + str(2)
                        num_entry = ClassParticipation.objects.filter(
                            participated_class=c).count()
                        d[e] = num_entry
                    if fill_class_num_child_14_less is True:
                        d[dp + '_c' + str(3)] = c.num
                        e = dp + '_e' + str(3)
                        num_entry = ClassParticipation.objects.filter(
                            participated_class=c).count()
                        d[e] = num_entry
            d[dp + "_champ"] = division.champion
            d[dp + "_rchamp"] = division.champion_reserve
    write_fillable_pdf("show/static/VHSA_Results_2015.pdf",
                       "show/static/VHSA_Final_Results.pdf", d)  # uses "VHSA_Results_2015.pdf" and populates it's fields with the info in data dict, then it saves this new populated pdf to "VHSA_Final_Results.pdf"

    # returns the populated pdf
    return render(request, 'final_results.html', {"filename": "show/static/VHSA_Final_Results.pdf"})

def populate_excel(request, show_date): #pragma: no cover
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=district-qualified-youth-registration.xls'

    rb = xlrd.open_workbook('show/static/district-qualified-youth-registration.xls')
    wb = copy(rb)
    sheet = wb.get_sheet(0)

    list_4h = []
    show = Show.objects.get(date=show_date)
    combos = HorseRiderCombo.objects.filter(show=show)
    for combo in combos:
        print (combo)
        if combo.rider.member_4H:
            horse_name = combo.horse.name
            entry = [combo.rider.first_name, combo.rider.last_name, horse_name.split("(", 1)[0], combo.rider.county]
            list_4h.append(entry)
    sorted_list_4h = sorted(list_4h, key=itemgetter(3, 1))
    style0 = xlwt.easyxf('font: bold on')
    style1 = xlwt.easyxf('font: bold on', num_format_str='D-MMM-YY')
    sheet.write(3, 2, show.name, style0)
    sheet.write(5, 2, show.location, style0)
    sheet.write(5, 4, show.date, style1)

    for i in range(0, len(sorted_list_4h)):
        for j in range(0,4):
            sheet.write(11+i, j, sorted_list_4h[i][j])

    wb.save(response)
    return response

def generate_labels(request, show_date): #pragma: no cover
    # view to execute label generating
    generate_show_labels(show_date)
    show = Show.objects.get(date=show_date)
    if(len(HorseRiderCombo.objects.filter(show=show))==0):
        messages.error(
                    request, "There are no Horse Rider Combos registered for this show.")
        context = {
            "show_name": show.name,
            "date": show_date,
            "location": show.location,
            "divisions": show.divisions.all(),
        }
        return render(request, 'view_show.html', context)
    else:
        generate_show_labels(show_date)
        return render(request, 'labels.html', {'date':str(show_date)})
