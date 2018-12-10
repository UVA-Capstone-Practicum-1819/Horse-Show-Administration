import random
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
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        requested_path = request.path
        excluded_urls = ["/show/login", "/show/signup", "/admin"]
        if not request.user.is_authenticated and requested_path not in excluded_urls:
            return redirect('login')
        # Code to be executed for each request/response after
        # the view is called.

        return response

def index(request):
    """
    Deprecated. The home page is now the show select page.
     """
    if 'navigation' in request.session:
        del request.session['navigation']
    if 'rider_pk' in request.session:
        del request.session['rider_pk']
    if 'horse_pk' in request.session:
        del request.session['horse_pk']
    latest_show_list = Show.objects.all
    template = loader.get_template('index.html')
    context = {
        'latest_show_list': latest_show_list,
    }
    return redirect('show_select')
    return HttpResponse(template.render(context, request))

#used as the home page for a selected show
def showpage(request, showdate):
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
    # template = loader.get_template('showpage.html')
    form = ComboNumForm()
    shows = Show.objects.all().order_by('date')
    context = {
        'form': form,
    }
    for show in shows:
        if showdate == show.date:
            context = {
                "name": show.name,
                "date": show.date,
                "location": show.location,
                "divisions": show.divisions.all,
                'form': form,
            }
    # return HttpResponse(template.render(context, request))
    return render(request, 'showpage.html', context)


# def classpage(request):
#     latest_show_list = Show.objects.all
#     template = loader.get_template('classpage.html')
#     context = {
#         'latest_show_list': latest_show_list,
#     }
#     return HttpResponse(template.render(context, request))

#view used to create the show, if successful, redirects to its show home page
def create_show(request):
    form = ShowForm()
    if request.method == "GET":
        return render(request, 'create_show.html', {'form': form})
    f = ShowForm(request.POST)
    if not f.is_valid():
        return render(request, 'create_show.html', {'form': f})
    showname = f.cleaned_data['name']
    showdate = f.cleaned_data['date']
    if Show.objects.filter(date=showdate).count() is 1:
        response = {'ok': True, 'success_msg': "Cannot have Shows with same date",
                    'form': form}
        return render(request, 'create_show.html', response, {'form': f})
    showdatestring = str(showdate)
    showlocation = f.cleaned_data['location']
    new_show = Show.objects.create(
        name=showname, date=showdatestring, location=showlocation,
        dayOfPrice=f.cleaned_data['dayOfPrice'], preRegistrationPrice=f.cleaned_data['preRegistrationPrice'])
    response = {'ok': True, 'success_msg': "Show was successfully created",
                'form': form, 'show': new_show}
    # return render(request, 'create_show.html', response)
    return redirect('showpage', showdate)

#view that allows the user to select a show
def show_select(request):
    if request.method == "POST":
        form = ShowSelectForm(request.POST)
        if form.is_valid():
            show = form.cleaned_data['date']
            show.date = show.date[:-3]
            showdate = show.date
            request.session['showdate'] = showdate
            return redirect('showpage', showdate)
    else:
        form = ShowSelectForm()
    return render(request, 'show_select.html', {'form': form})

#Autocomplete functionality for the select page
class ShowAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
            # return Horse.objects.none()
        qs = Show.objects.all().order_by('date')
        if self.q:
            qs = qs.filter(show_name__istartswith=self.q)
        return qs


def signup(request):
    """ signs up the user (creates an account) """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('show_select')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

#Autocomplete functionality for selecting a combo
class ComboAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = HorseRiderCombo.objects.all().order_by('num')
        if self.q:
            qs = qs.filter(class_name__istartswith=self.q)
        return qs

#Used to retrieve information necessary for billing a rider
def billing(request, showdate):
    if request.method == "POST":
        form = ComboSelectForm(request.POST)
        # allows the user to select from the pre-existing horse-rider combos
        if form.is_valid():
            combo = form.cleaned_data['combo']
            combonum = combo.num
            return redirect('billinglist', showdate, combonum)
    else:
        form = ComboSelectForm()
    return render(request, 'billing.html', {'form': form, 'date': showdate})

#Billing list shows what horse rider combos need to be billed for and their total price
def billinglist(request, showdate, combonum):
    show = Show.objects.get(date=showdate)
    # form = RegistrationBillForm()
    combo = HorseRiderCombo.objects.get(num=combonum)
    tot = combo.classes.count()
    price = show.preRegistrationPrice * tot
    # for minimum requirements, only calculates price based on pre-registration price
    context = {'name': combo.rider, 'show_date': show.date,
     'classes': combo.classes.all, 'combo_num': combo.num, 'tot': tot, 'price': price}
    # the context will help create the table for the list of classes a user is currently in
    return render(request, 'billinglist.html', context)

#This view allows you to scratch from a show
def scratch(request, showdate, combonum):
    # combonum = request.GET['combonum']
    # showdate = request.GET['showdate']
    # print(combonum+1)
    show = Show.objects.get(date=showdate)
    combo = HorseRiderCombo.objects.get(num=int(combonum))
    cls = request.GET["cname"]
    dcls = combo.classes.get(name=cls)
    combo.classes.remove(dcls)
    # this line allows for a classes to be scratched (or removed) at no additional cost
    # the list will be changed based on what classes were removed
    # classes will only be removed from the horse-rider combo object, not from the entire database
    tot = combo.classes.count()
    price = show.preRegistrationPrice * tot
    context = {'name': combo.rider, 'show_date': show.date,
      'classes': combo.classes.all, 'combo_num': combo.num, 'tot': tot, 'price': price}
    # context information need to populate table
    return render(request, 'billinglist.html', context)
    # rendered to the same html page


def divisionscore(request,divisionname): #displays list of classes in division, hrc winners of each of those classes from 1st-6th places, and form to enter champion info
    division = Division.objects.get(name= divisionname) # get the division object from the name of the divison that was passed in
    form = DivisionChampForm()
    if request.method == "POST":
        form = DivisionChampForm(request.POST)
        if form.is_valid():
            champion= form.cleaned_data['champion']
            champion_pts= form.cleaned_data['champion_pts']
            champion_reserve= form.cleaned_data['champion_reserve']
            champion_reserve_pts= form.cleaned_data['champion_reserve_pts']
            division.champion= champion #sets the division's champion field  equal to the value entered into the "champion" field of the DivisionChampForm
            division.champion_pts= champion_pts #sets the division's champion_pts field equal to the value entered into the "champion_pts" field of DivisionChampForm
            division.champion_reserve= champion_reserve #sets the division's champion_reserve field equal to the value entered into the "champion_reserve" field of DivisionChampForm
            division.champion_reserve_pts= champion_reserve_pts #sets the division's champion_reserve_pts field equal to the value entered into the "champion_reserve_pts" field of DivisionChampForm
            division.save() #saves the division object fields in the database

    else:
        form = DivisionChampForm()
    context = {'classes': division.classes.all, 'name': division.name, 'form': form}
    return render(request, 'division_score.html', context) #passes the DivisionChampForm and the division's name and classes to "division_score.html" and renders that page

def delete_class(request, showdate, divisionname, classnumber): #deletes a class from a division
    division = Division.objects.get(name=divisionname) #gets the division object from the division name that was passed in
    classObj = Classes.objects.get(number=classnumber)
    division.classes.remove(classObj)
    classObj.delete() #removes the class object from the division's many-to-many "classes" field
    division.save() #saves the division object in the database
    context = {'classes': division.classes.all,'name': division.name}
    return redirect('division_info', showdate=showdate, divisionname=divisionname)  #redirects to division_classes and passes in the division's name


def division_classes(request,divisionname): #lists the classes in a division
    division = Division.objects.get(name= divisionname)  #gets the division object from the division name that was passed in
    context = {'classes': division.classes.all,'name': division.name}
    return render(request, 'division_classes.html', context) #passes the division's name and classes to the "division_classes.html" and renders that page


#This view allows you to add a new class
def new_class(request):
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            existing_classes = Classes.objects.all()
            for cl in existing_classes:
                if cl.number == form.cleaned_data['number']:
                    messages.error(request, "class number in use")
                    return redirect('classes')
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # return render(request, 'editrider.html', {'form': form})
            return redirect('/show/class')
    else:
        form = ClassForm()
    return render(request, 'new_class.html', {'form': form})

#This view allows you to select a class from a prepopulated list
def class_select(request):
    if request.method == "POST":
        form = ClassSelectForm(request.POST)
        if form.is_valid():
            classobj = form.cleaned_data['selected_class']
            classname = classobj.name
            request.session['classobj'] = classname
            return redirect('rankclass', classname)
    else:
        form = ClassSelectForm()
    return render(request, 'class_select.html', {'form': form})

#This method ranks classes from 1st through 6th and stores the winning scores under
#specific horse rider combos that competed in that class and were awarded points
#points are always starting from 10, then 6, and so on
def rankclass(request, classname):
    if request.method == 'POST':
        # if 'classobj' in request.session:
        #     classtoscore = request.session['classobj']
        #classtoscore = request.POST.get('name', None)
        form = RankingForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['first']
            second = form.cleaned_data['second']
            third = form.cleaned_data['third']
            fourth = form.cleaned_data['fourth']
            fifth = form.cleaned_data['fifth']
            sixth = form.cleaned_data['sixth']
            showclass = Classes.objects.get(name=classname)
            showclass.first = first
            showclass.second = second
            showclass.third = third
            showclass.fourth = fourth
            showclass.fifth = fifth
            showclass.sixth = sixth
            showclass.save()
            firstcombo = HorseRiderCombo.objects.get(num=first)

            firstscore = ClassScore.objects.create(participated_class=showclass, score=10)
            firstcombo.class_scores.add(firstscore)
            secondcombo = HorseRiderCombo.objects.get(num=second)
            secondscore = ClassScore.objects.create(participated_class=showclass, score=6)
            secondcombo.class_scores.add(secondscore)
            thirdcombo = HorseRiderCombo.objects.get(num=third)
            thirdscore = ClassScore.objects.create(participated_class=showclass, score=4)
            thirdcombo.class_scores.add(thirdscore)
            fourthcombo = HorseRiderCombo.objects.get(num=fourth)
            fourthscore = ClassScore.objects.create(participated_class=showclass, score=2)
            fourthcombo.class_scores.add(fourthscore)
            fifthcombo = HorseRiderCombo.objects.get(num=fifth)
            fifthscore = ClassScore.objects.create(participated_class=showclass, score=1)
            fifthcombo.class_scores.add(fifthscore)
            sixthcombo = HorseRiderCombo.objects.get(num=sixth)
            sixthscore = ClassScore.objects.create(participated_class=showclass, score=0.5)
            sixthcombo.class_scores.add(sixthscore)
            if 'showdate' in request.session:
                showdate = request.session['showdate']
                return redirect('showpage', showdate)
            # will redirect with a class rank page
    else:
        form = RankingForm()
        return render(request, 'rankclass.html', {'form': form})

#This is the autocomplete functionality for selecting a class
class ClassAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Classes.objects.all().order_by('number')
        if self.q:
            qs = qs.filter(class_name__istartswith=self.q)
        return qs

def new_division(request, showdate):
    """ Form for allowing users to create a new division, which is a subset of show """
    show = Show.objects.get(date=showdate)
    date = show.date
    if request.method == "POST":
        if 'exit' in request.POST:
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
                return redirect('showpage', date)
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
    else:
        form = DivisionForm()
        show = Show.objects.get(date=showdate)
        context = {
            "form": form,
            "name": show.name,
            "date": show.date,
            "location": show.location,
            "divisions": show.divisions.all,
        }
        return render(request, 'new_division.html', context)

def division(request, showdate, divisionname):
    """ Info about divisions/classes in a show """
    show = Show.objects.get(date=showdate)
    division = Division.objects.get(name=divisionname)
    if request.method == 'POST': #if POST, create a new class for this division
        form = AddClassForm(request.POST)
        if form.is_valid():
            existing_classes = Classes.objects.all() #verify number doesnt already exist
            for cl in existing_classes: #number is not a primary key because theoretically, multiple shows should be able to have class number 2. 
                if cl.number == form.cleaned_data['number']: #compare
                    messages.error(request, "class number in use") #prepare error message, will display on submit.
                    return redirect('division_info', showdate, divisionname)
            c = Classes(name=form.cleaned_data['name'], number=form.cleaned_data['number'])
            c.save()
            division = Division.objects.get(name=divisionname)
            # division_classes = division.classes.all()
            # division_classes.add(c)
            division.classes.add(c) #add class to that division 
            # division.classes = division_classes
            division.save()
            return redirect('division_info', showdate, divisionname) #render page with new division
    else:
        if(len(division.classes.all()) < 3): #each division only has a max of 3 classes, no input form if 3 classes present
            form = AddClassForm() 
            context = {
                "form": form,
                "showdate" : showdate,
                "showname": show.name,
                "division": division.name,
                "classes": division.classes.all(),
            }
        else:
            context = {
                "showdate":show.date,
                "showname": show.name,
                "division": division.name,
                "classes": division.classes.all(),
            }
        return render(request, 'division.html', context)

def class_info(request, showdate, divisionname, classnumber):  #render class info including combos in class
    show = Show.objects.get(date=showdate)
    division = Division.objects.get(name=divisionname)
    this_class = Classes.objects.get(number = classnumber)
    this_combos = [] #will hold combos of class
    combos = HorseRiderCombo.objects.all()
    for combo in combos: #iterate through combos to find matches//perhaps make a manytomany field later, but was told not to change models 
        classes = combo.classes.all()
        for c in classes:
            if c == this_class:
                this_combos.append(combo) #add if class in combo.classes
    context = {
        "combos":this_combos,
        "number":this_class.number,
        "date":showdate,
        "name":divisionname,
        "showname":show.name,
    }
    return render(request, "classpage.html", context) #render info

def delete_combo(request, showdate, divisionname, classnumber, combo): #scratch a combo from the class page so that it reflects in the combo's billing
    combo = HorseRiderCombo.objects.get(num=combo) 
    classObj = Classes.objects.get(number=classnumber)
    combo.classes.remove(classObj)
    return redirect('edit_class', showdate=showdate, divisionname=divisionname, classnumber=classnumber)

def division_select(request, showdate): #displays division select dropdown and ability to "Save" or "See Division Scores"
    if request.method == "POST":
        if 'save' in request.POST: #if a division is selected and the "Save" button is clicked
            form = DivisionSelectForm(request.POST)
            if form.is_valid():
                print("form valid ")
                show = Show.objects.get(date=showdate)
                current_divisions = show.divisions
                division = Division.objects.get(
                    name=form.cleaned_data['name'])
                current_divisions.add(division)
                show.save() #saves the show ohject in the database

                divisionname= division.name

                # return render(request, 'horse_select.html', {'form': form})
                # return redirect('/')
                #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                return redirect('division_classes', divisionname)
        if 'score' in request.POST: # if a division is selected and the "See Divison Scores" button is clicked
            form = DivisionSelectForm(request.POST)
            if form.is_valid():
                division = Division.objects.get(
                    name=form.cleaned_data['name']) # get the division object from the "name" field in the DivisionSelectFrom
                divisionname = division.name
                return redirect('divisionscore', divisionname) #redirects to divisionscore and passes in the divisionname

    else:
        form = DivisionSelectForm()
    return render(request, 'division_select.html', {'form': form, 'date': showdate})

class DivisionAutocomplete(autocomplete.Select2QuerySetView):
    """ fills in form automatically based on value entered by user """
    def get_queryset(self):
        qs = Division.objects.all().order_by('number')
        if self.q:
            qs = qs.filter(division_name__istartswith=self.q)
        return qs

def select_rider(request):
    """ selects a rider from a dropdown and stores its primary key into a session """
    if request.method == "POST":
        request.session['rider_pk'] = request.POST['rider']
        return redirect('select_horse')
    form = RiderSelectForm()
    return render(request, 'rider_select.html', {'form': form})

def select_rider2(request):
    """ select rider function exclusively for editing a rider """
    if request.method == "POST":
        rider_pk = request.POST['rider']
        return redirect('edit_rider', rider_pk=rider_pk)
    form = RiderSelectForm()
    return render(request, 'rider_select2.html', {'form': form})

def edit_rider(request, rider_pk):
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
    return render(request, 'rider_edit.html', {'rider': rider, 'edit_rider_form': edit_rider_form})

def add_rider(request):
    """ creates a new rider in a form and stores its primary key into a session, then redirects to select_horse """
    if request.method == "POST":
        form = RiderForm(request.POST)
        if form.is_valid():
            rider = form.save()
            request.session['rider_pk'] = rider.pk
            return redirect('select_horse')
    form = RiderForm()
    return render(request, 'editrider.html', {'form': form})

def select_horse2(request):
    """ select horse function exclusively for editing a horse """
    if request.method == "POST":
        horse_pk = request.POST['horse']
        return redirect('edit_horse', horse_pk=horse_pk)
    form = HorseSelectForm()
    return render(request, 'horse_select2.html', {'form': form})

def edit_horse(request, horse_pk):
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
    return render(request, 'horse_edit.html', {'horse': horse, 'edit_horse_form': edit_horse_form})

def add_horse(request):
    """ creates a new horse in a form and stores its primary key into a session, then redirects to add_combo """
    if request.method == "POST":
        form = HorseForm(request.POST)
        if form.is_valid():
            horse = form.save()
            request.session['horse_pk'] = horse.pk
            return redirect('add_combo')
    form = HorseForm()
    return render(request, 'horse_add.html', {'form': form})

#This view shows the autocomplete functionality for selection a rider
class RiderAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Rider.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def select_horse(request):
    """ selects a horse from a dropdown and stores its primary key into a session """
    if request.method == 'POST':
        horse = request.POST['horse']
        request.session['horse_pk'] = request.POST['horse']
        return redirect('add_combo')
    form = HorseSelectForm()
    return render(request, 'horse_select.html', {'form': form})




def add_combo(request):
    """
        creates a page for adding a horse-rider combination, taking in the session variables for the primary keys of the chosen horse and rider
        redirects to the edit combo page for the same combination after it is done
     """
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
            HorseRiderCombo.objects.create(num=num, rider=rider, horse=horse, cell=cell, email=email)
            return redirect('edit_combo', num=num)
        else:
            return redirect('show_select')
    rider_pk = request.session['rider_pk']
    if rider_pk is None:
        return redirect('show_select')
    horse_pk = request.session['horse_pk']
    if horse_pk is None:
        return redirect('show_select')
    rider = get_object_or_404(Rider, pk=rider_pk)
    horse = get_object_or_404(Horse, pk=horse_pk)
    form = HorseRiderComboCreateForm()
    return render(request, 'add_combo.html', {'form': form, 'rider': rider, 'horse': horse})

def edit_combo(request, num):
    """
    edits the combination that was specified by num
    also handles the addition/removal of classes and the calculation of price
     """
    combo = HorseRiderCombo.objects.get(pk=num)
    if request.method == "POST":
        if request.POST.get('remove_class'):
            num = request.POST['remove_class']
            selected_class = Classes.objects.get(number=num)
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


    edit_form = HorseRiderEditForm({'email': combo.email, 'cell': combo.cell, 'contact': combo.contact}, instance=combo)

    class_selection_form = ClassSelectForm()

    registered_classes = combo.classes.all()
    number_registered_classes = len(registered_classes)
    price = number_registered_classes * 10

    return render(request, 'edit_combo.html', {'combo': combo, 'edit_form': edit_form, 'class_selection_form': class_selection_form, 'classes': registered_classes, 'price': price, 'tot': number_registered_classes})



def check_combo(request, num):
    """
    Deprecated. edit_combo now accomplishes this functions' tasks
     """
    if request.method == "POST":
        rider = HorseRiderCombo.objects.get(pk=num).rider
        horse = HorseRiderCombo.objects.get(pk=num).horse
        return render(request, 'class_select.html')
    return render(request, 'check_combo.html', {'num': num, 'rider': rider, 'horse': horse})
    # return redirect(reverse('index'))

#This view shows the autocomplete functionality for selecting a horse
class HorseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Horse.objects.all().order_by('name') #orders horses in dropdown queryset by name

        if self.q:
            qs = qs.filter(name__istartswith=self.q) #filters horses in dropdown queryset by checking if horses' names start with the text entered into the field

        return qs


# def new_class(request):
#     print(request.method)
#     if request.method == "POST":
#         form = ClassesForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             # return redirect('horse_detail', pk=post.pk)
#             return render(request, 'classes.html', {'form': form})
#     else:
#         form = ClassesForm()
#     return render(request, 'classes.html', {'form': form})
#

#This function will be implemented later for desired requirements. Used to populate pdfs for horse show reports
def populate_pdf(request): #populates text fields of PDF
    data_dict = {
        'show': '11/7/2018',
        'judge': 'Bertha',
    } #info to populate the pdf's "show" and "judge" text fields
    write_fillable_pdf("show/static/VHSA_Results_2015.pdf",
                       "show/static/VHSA_Final_Results.pdf", data_dict) #uses "VHSA_Results_2015.pdf" and populates it's fields with the info in data dict, then it saves this new populated pdf to "VHSA_Final_Results.pdf"

    return render(request, 'finalresults.html', {"filename": "show/static/VHSA_Final_Results.pdf"}) #returns the populated pdf
