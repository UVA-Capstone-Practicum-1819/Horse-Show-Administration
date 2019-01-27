import random
import re
import os
import json
import pdfrw
import datetime
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import resolve, reverse
from show.forms import *
from django.contrib.auth import views as auth_views
from django.forms.models import model_to_dict
from show.models import *
from django.utils import timezone
from dal import autocomplete
from .populatepdf import write_fillable_pdf
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


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
        if re.match(r'/show.*', requested_path) and not requested_path == "/show/login" and not request.user.is_authenticated:
            return redirect('log_in')

        return response


def view_show(request, show_date):
    """ used as the home page for a selected show """
    if request.method == "POST":
        form = ComboNumForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['num']
            return redirect('edit_combo', num=num)
    if 'navigation' in request.session:
        del request.session['navigation']
    if 'rider_pk' in request.session:
        del request.session['rider_pk']
    if 'horse_pk' in request.session:
        del request.session['horse_pk']
    form = ComboNumForm()

    show = Show.objects.get(date=show_date)

    context = {
        "show_name": show.name,
        "date": show_date,
        "location": show.location,
        "divisions": show.divisions.all(),
        'form': form,
    }
    return render(request, 'view_show.html', context)


def add_show(request):
    """ view used to create the show, if successful, redirects to its show home page """
    form = ShowForm()
    if request.method == "GET":
        return render(request, 'add_show.html', {'form': form})
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



def select_show(request):
    """ view that allows the user to select a show """
    if request.method == "POST":
        form = ShowSelectForm(request.POST)
        if form.is_valid():
            show = form.cleaned_data['date']
            show.date = show.date[:-3]
            show_date = show.date
            request.session['show_date'] = show_date
            return redirect('view_show', show_date)
    else:
        form = ShowSelectForm()
    return render(request, 'select_show.html', {'form': form})


def sign_up(request):
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
    """ Billing list shows what horse rider combos need to be billed for and their total price """
    show = Show.objects.get(date=show_date)
    combo = show.combos.filter(num=combo_num)[0]
    classes = combo.classes
    tot = classes.count()
    price = show.pre_reg_price * tot
    # for minimum requirements, only calculates price based on pre-registration price
    context = {'name': combo.rider, 'show_date': show_date,
               'classes': classes.all(), 'combo_num': combo_num, 'tot': tot, 'price': price}
    # the context will help create the table for the list of classes a user is currently in
    return render(request, 'view_billing.html', context)


def scratch_combo(request, show_date, combo_num):
    """ This view allows you to scratch from a show """
    show = Show.objects.get(date=show_date)
    combo = show.combos.filter(num=combo_num)[0]
    cls = request.GET["cname"]
    dcls = combo.classes.get(name=cls)
    combo.classes.remove(dcls)
    # this line allows for a classes to be scratched (or removed) at no additional cost
    # the list will be changed based on what classes were removed
    # classes will only be removed from the horse-rider combo object, not from the entire database
    tot = combo.classes.count()
    price = show.pre_reg_price * tot
    context = {'name': combo.rider, 'show_date': show_date,
               'classes': combo.classes.all(), 'combo_num': combo_num, 'tot': tot, 'price': price}
    # context information need to populate table
    return render(request, 'view_billing.html', context)
    # rendered to the same html page


def view_division_scores(request, show_date, division_name):
    """ displays list of classes in division, hrc winners of each of those classes from 1st-6th places, and form to enter champion info """
    show = Show.objects.get(date=show_date)
    # get the division object from the name of the divison that was passed in
    division = show.divisions.filter(name=division_name)[0]
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
    context = {'classes': division.classes.all(),
               'name': division.name, 'form': form}
    # passes the DivisionChampForm and the division's name and classes to "division_score.html" and renders that page
    return render(request, 'division_score.html', context)


def delete_class(request, show_date, division_name, class_num):
    """ deletes a class from a division """
    show = Show.objects.get(date=show_date)
    division = show.divisions.filter(name=division_name)[0]
    class_obj = division.classes.filter(num=class_num)[0]
    # gets the division object from the division name that was passed in
    class_obj.delete()  # removes the class object
    # redirects to division_classes and passes in the division's name
    return redirect('view_division', show_date=show_date, division_name=division_name)


def view_division_classes(request, show_date, division_name):
    """ lists the classes in a division """
    show = Show.objects.get(date=show_date)
    division = show.divisions.filter(name=division_name)[0]
    context = {'classes': division.classes.all(), 'name': division_name}
    # passes the division's name and classes to the "division_classes.html" and renders that page
    return render(request, 'view_division_classes.html', context)


def add_class(request, show_date, division_name):
    """ This view allows you to add a new class """
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            show = Show.objects.get(date=show_date)
            division = show.divisions.filter(name=division_name)[0]
            existing_classes = division.classes.filter(
                num=form.cleaned_data['num'])
            if existing_classes:
                messages.error(request, "class number in use")
                return redirect('view_division_classes', show_date=show_date, division_name=division_name)

            return redirect('/show/class')
    else:
        form = ClassForm()
    return render(request, 'add_class.html', {'form': form})


def select_class(request, show_date, division_name):
    """ This view allows you to select a class from a prepopulated list """
    if request.method == "POST":
        form = ClassSelectForm(request.POST)
        if form.is_valid():
            class_num = form.cleaned_data['num']
            #request.session['class_obj'] = class_name
            return redirect('rank_class', class_num)
    else:
        form = ClassSelectForm()
    return render(request, 'select_class.html', {'form': form})


def rank_class(request, show_date, division_name, class_num):
    """ 
        This method ranks classes from 1st through 6th and stores the winning scores under    
        specific horse rider combos that competed in that class and were awarded points
        points are always starting from 10, then 6, and so on
    """
    if request.method == 'POST':

        form = RankingForm(request.POST)
        if form.is_valid():
            combo_map = {
                form.cleaned_data['first']: 10,
                form.cleaned_data['second']: 6,
                form.cleaned_data['third']: 4,
                form.cleaned_data['fourth']: 2,
                form.cleaned_data['fifth']: 1,
                form.cleaned_data['sixth']: 0.5,
            }
            show = Show.objects.get(date=show_date)
            division = show.divisions.filter(name=division_name)[0]
            class_obj = division.classes.filter(num=class_num)[0]

            participations = class_obj.participations.all()

            for participation in participations:
                combo_num = participation.combo.num
                if combo_num in combo_map:
                    participation.score = combo_map[combo_num]
                    participation.save()

            return redirect('view_class', show_date=show_date, division_name=division_name, class_num=class_num)

            # will redirect with a class rank page
    else:
        form = RankingForm()
        return render(request, 'rank_class.html', {'form': form})


def add_division(request, show_date):
    """ Form for allowing users to create a new division, which is a subset of show """
    show = Show.objects.get(date=show_date)

    if request.method == "POST":
        form = DivisionForm(request.POST)
        if form.is_valid():
            divisions = Division.objects.filter(name=form.cleaned_data['name'])
            if(len(divisions) > 0):
                # prepare error message, will display on submit.
                messages.error(request, "division number in use")
                return redirect('divisions', show_date)
            division_form = DivisionForm(request.POST)
            division = division_form.save(commit=False)
            division.show = show
            division.save()
        if 'another' in request.POST:
            form = DivisionForm(request.POST)
            if form.is_valid():
                divisions = Division.objects.filter(number=form.cleaned_data['number'])
                if(len(divisions) > 0):
                    messages.error(request, "division number in use") #prepare error message, will display on submit.
                    return redirect('divisions', showdate)
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                division = Division.objects.get(
                    name=form.cleaned_data['name'])
                divisions = show.divisions
                divisions.add(division)
                show.save()
                return redirect('divisions', showdate)

        if 'class_add' in request.POST:
            form = DivisionForm(request.POST)
            if form.is_valid():
                divisions = Division.objects.filter(number=form.cleaned_data['number'])
                if(len(divisions) > 0):
                    messages.error(request, "division number in use") #prepare error message, will display on submit.
                    return redirect('divisions', showdate)
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                division = Division.objects.get(
                    name=form.cleaned_data['name'])
                divisions = show.divisions
                divisions.add(division)
                show.save()
                return redirect('division_info', showdate, division)
            return redirect('add_division', show_date)
        elif 'exit' in request.POST:
            return redirect('view_show', show_date)
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


def view_division(request, show_date, division_name):
    """ Info about divisions/classes in a show """
    show = Show.objects.get(date=show_date)
    division = show.divisions.filter(name=division_name)[0]
    if request.method == 'POST':  # if POST, create a new class for this division
        form = ClassForm(request.POST)
        if form.is_valid():
            existing_classes_count = division.classes.filter(
                num=form.cleaned_data['num']).count()
            # verify number doesnt already exist
            if existing_classes_count > 0:
                # prepare error message, will display on submit.
                messages.error(request, "class number in use")
                return redirect('division_info', show_date, division_name)

            class_form = ClassForm(request.POST)
            class_obj = class_form.save(commit=False)
            class_obj.division = division
            class_obj.save()
            # render page with new division
            return redirect('view_division', show_date=show_date, division_name=division_name)
    else:
        # each division only has a max of 3 classes, no input form if 3 classes present
        division_classes = division.classes.all()
        context = {
            "date": show_date,
            "show_name": show.name,
            "name": division_name,
            "classes": division_classes,
        }
        if(len(division_classes) < 3):
            form = ClassForm()
            context['form'] = form
        print("THIS IS THE DIVISION: " + division_name)
        return render(request, 'view_division.html', context)


def view_class(request, show_date, division_name, class_num):
    """ render class info including combos in class """
    show = Show.objects.get(date=show_date)
    division = show.divisions.filter(name=division_name)[0]
    class_obj = division.classes.filter(num=class_num)[0]
    combos = class_obj.combos.all()
    """ for combo in combos:  # iterate through combos to find matches//perhaps make a manytomany field later, but was told not to change models
        classes = combo.classes.all()
        for c in classes:
            if c == class_obj:
                this_combos.append(combo)  # add if class in combo.classes """
    context = {
        "combos": combos,
        "number": class_num,
        "date": show_date,
        "name": division_name,
        "show_name": show.name,
    }
    return render(request, "view_class.html", context)  # render info


def delete_combo(request, show_date, division_name, class_num, combo):
    """ scratch a combo from the class page so that it reflects in the combo's billing """
    combo = HorseRiderCombo.objects.get(num=combo)
    show = Show.objects.get(date=show_date)
    division = show.divisions.filter(name=division_name)[0]
    class_obj = division.classes.filter(num=class_num)[0]
    combo.classes.remove(class_obj)
    return redirect('view_class', date=show_date, division_name=division_name, class_num=class_num)


def select_division(request, show_date):
    """ displays division select dropdown and ability to "Save" or "See Division Scores" """
    if request.method == "POST":

        if 'save' in request.POST:  # if a division is selected and the "Save" button is clicked
            form = DivisionSelectForm(request.POST)
            if form.is_valid():
                show = Show.objects.get(date=show_date)
                return redirect('view_division_classes', show_date=show_date, division_name=form.cleaned_data['name'])
        if 'score' in request.POST:  # if a division is selected and the "See Divison Scores" button is clicked
            form = DivisionSelectForm(request.POST)
            if form.is_valid():
                # redirects to divisionscore and passes in the division_name
                return redirect('view_division_scores', show_date=show_date, division_name=form.cleaned_data['name'])

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
    return render(request, 'select_rider2.html', {'form': form, 'show_date': show_date})


def edit_rider(request, show_date, rider_pk):
    """ allows user to change the given fields in rider and save changes """
    rider = Rider.objects.get(pk=rider_pk)
    if request.method == "POST":
        edit_form = RiderEditForm(request.POST)
        if edit_form.is_valid():
            rider.name = edit_form.cleaned_data['name']
            rider.address = edit_form.cleaned_data['address']
            rider.birth_date = edit_form.cleaned_data['birth_date']
            rider.member_VHSA = edit_form.cleaned_data['member_VHSA']
            rider.county = edit_form.cleaned_data['county']
            rider.save()

    edit_rider_form = RiderEditForm(
        {'name': rider.name, 'address': rider.address,
         'birth_date': rider.birth_date, 'member_VHSA': rider.member_VHSA, 'county': rider.county},
        instance=rider)
    return render(request, 'edit_rider.html', {'rider': rider, 'edit_rider_form': edit_rider_form, 'date': show_date})


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
            horse.accession_no = edit_form.cleaned_data['accession_no']
            horse.coggins_date = edit_form.cleaned_data['coggins_date']
            horse.owner = edit_form.cleaned_data['owner']
            horse.type = edit_form.cleaned_data['type']
            horse.size = edit_form.cleaned_data['size']
            horse.save()

    edit_horse_form = HorseEditForm(
        {'accession_no': horse.accession_no, 'coggins_date': horse.coggins_date,
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


def add_combo(request, show_date):
    """
        creates a page for adding a horse-rider combination, taking in the session variables for the primary keys of the chosen horse and rider
        redirects to the edit combo page for the same combination after it is done
     """
    show = Show.objects.get(date=show_date)
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
            HorseRiderCombo.objects.create(
                num=num, rider=rider, horse=horse, cell=cell, email=email, show=show)
            return redirect('edit_combo', show_date=show_date, combo_num=num)
        else:
            return redirect('view_show', show_date=show_date)
    rider_pk = request.session['rider_pk']
    if rider_pk is None:
        return redirect('select_show')
    horse_pk = request.session['horse_pk']
    if horse_pk is None:
        return redirect('select_show')
    rider = get_object_or_404(Rider, pk=rider_pk)
    horse = get_object_or_404(Horse, pk=horse_pk)
    form = HorseRiderComboCreateForm()
    return render(request, 'add_combo.html', {'form': form, 'rider': rider, 'horse': horse, 'date': show_date})


def edit_combo(request, show_date, combo_num):
    """
    edits the combination that was specified by num
    also handles the addition/removal of classes and the calculation of price
     """
    show = Show.objects.get(date=show_date)
    combo = show.combos.filter(num=combo_num)[0]
    if request.method == "POST":
        if request.POST.get('remove_class'):
            num = request.POST['remove_class']
            selected_class = Class.objects.get(pk=num)
            combo.classes.remove(selected_class)
            combo.save()

        if request.POST.get('add_class'):
            class_selection_form = ClassSelectForm(request.POST)

            if class_selection_form.is_valid():
                selected_class = class_selection_form.cleaned_data['selected_class']
                combo.classes.add(selected_class)
                combo.save()

        elif request.POST.get('edit'):
            edit_form = HorseRiderEditForm(request.POST)

            if edit_form.is_valid():
                combo.email = edit_form.cleaned_data['email']
                combo.cell = edit_form.cleaned_data['cell']
                combo.contact = edit_form.cleaned_data['contact']
                combo.save()

    edit_form = HorseRiderEditForm(
        {'email': combo.email, 'cell': combo.cell, 'contact': combo.contact}, instance=combo)

    class_selection_form = ClassSelectForm()

    registered_classes = combo.classes.all()
    number_registered_classes = len(registered_classes)
    price = number_registered_classes * 10

    return render(request, 'edit_combo.html', {'combo': combo, 'edit_form': edit_form, 'class_selection_form': class_selection_form, 'classes': registered_classes, 'price': price, 'tot': number_registered_classes, 'date': show_date})


def populate_pdf(request, show_date):
    """ This function will be implemented later for desired requirements. Used to populate pdfs for horse show reports """
    data_dict = {
        'show': '11/7/2018',
        'judge': 'Bertha',
    }  # info to populate the pdf's "show" and "judge" text fields
    write_fillable_pdf("show/static/VHSA_Results_2015.pdf",
                       "show/static/VHSA_Final_Results.pdf", data_dict)  # uses "VHSA_Results_2015.pdf" and populates it's fields with the info in data dict, then it saves this new populated pdf to "VHSA_Final_Results.pdf"

    # returns the populated pdf
    return render(request, 'final_results.html', {"filename": "show/static/VHSA_Final_Results.pdf"})


class ShowAutocomplete(autocomplete.Select2QuerySetView):
    """ Autocomplete functionality for the select page """

    def get_queryset(self):
        # if not self.request.user.is_authenticated():
            # return Horse.objects.none()
        qs = Show.objects.all().order_by('date')
        if self.q:
            qs = qs.filter(show_name__istartswith=self.q)
        return qs


class ComboAutocomplete(autocomplete.Select2QuerySetView):
    """ Autocomplete functionality for selecting a combo """

    def get_queryset(self):
        qs = HorseRiderCombo.objects.all().order_by('num')
        if self.q:
            qs = qs.filter(class_name__istartswith=self.q)
        return qs


class ClassAutocomplete(autocomplete.Select2QuerySetView):
    """ This is the autocomplete functionality for selecting a class """

    def get_queryset(self):
        qs = Class.objects.all().order_by('number')
        if self.q:
            qs = qs.filter(class_name__istartswith=self.q)
        return qs


class RiderAutocomplete(autocomplete.Select2QuerySetView):
    """ This view shows the autocomplete functionality for selection a rider """

    def get_queryset(self):
        qs = Rider.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class HorseAutocomplete(autocomplete.Select2QuerySetView):
    """ This view shows the autocomplete functionality for selecting a horse """

    def get_queryset(self):
        # orders horses in dropdown queryset by name
        qs = Horse.objects.all().order_by('name')

        if self.q:
            # filters horses in dropdown queryset by checking if horses' names start with the text entered into the field
            qs = qs.filter(name__istartswith=self.q)

        return qs


class DivisionAutocomplete(autocomplete.Select2QuerySetView):
    """ fills in form automatically based on value entered by user """

    def get_queryset(self):
        qs = Division.objects.all()
        if self.q:
            qs = qs.filter(division_name__istartswith=self.q)
        return qs
