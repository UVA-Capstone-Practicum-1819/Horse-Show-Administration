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
from django.forms.models import model_to_dict
from show.models import *
from django.utils import timezone
from dal import autocomplete
""" for authentication/signin/signup purposes """
from .populatepdf import write_fillable_pdf
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


class AuthRequiredMiddleware(object):
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
    return HttpResponse(template.render(context, request))


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


def classpage(request):
    latest_show_list = Show.objects.all
    template = loader.get_template('classpage.html')
    context = {
        'latest_show_list': latest_show_list,
    }
    return HttpResponse(template.render(context, request))


def create_show(request):
    form = ShowForm()
    if request.method == "GET":
        return render(request, 'create_show.html', {'form': form})
    f = ShowForm(request.POST)
    if not f.is_valid():
        return render(request, 'create_show.html', {'form': f})
    showname = f.cleaned_data['name']
    showdate = f.cleaned_data['date']
    showdatestring = str(showdate)
    showlocation = f.cleaned_data['location']
    new_show = Show.objects.create(
        name=showname, date=showdatestring, location=showlocation)
    response = {'ok': True, 'success_msg': "Show was successfully created",
                'form': form, 'show': new_show}
    return render(request, 'create_show.html', response)


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


class ShowAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
            # return Horse.objects.none()
        qs = Show.objects.all().order_by('date')
        if self.q:
            qs = qs.filter(show_name__istartswith=self.q)
        return qs


def signup(request):
    """ signs user up via form """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class ComboAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = HorseRiderCombo.objects.all().order_by('num')
        if self.q:
            qs = qs.filter(class_name__istartswith=self.q)
        return qs


def billing(request, showdate):
    if request.method == "POST":
        form = ComboSelectForm(request.POST)
        if form.is_valid():
            combo = form.cleaned_data['combo']
            combonum = combo.num
            return redirect('billinglist', showdate, combonum)
    else:
        form = ComboSelectForm()
    return render(request, 'billing.html', {'form': form, 'date': showdate})


def billinglist(request, showdate, combonum):
    show = Show.objects.get(date=showdate)
    # form = RegistrationBillForm()
    combo = HorseRiderCombo.objects.get(num=combonum)
    tot = combo.classes.count()

    price = show.preRegistrationPrice * tot
    #
    # if request.method == "POST":
    #     print("posting")
    #     if 'scratch' in request.POST:
    #         # combonum = request.GET['combonum']
    #         # combo = HorseRiderCombo.objects.get(num=int(combonum))
    #         clsnm = request.POST.get("cname")
    #         print(clsnm)
    #         dcls = combo.classes.get(name=clsnm)
    #         combo.classes.remove(dcls)
    #         tot = combo.classes.count()
    #         combo.save()
    #         context = {'name': combo.rider, 'show_date': show.date,
    #          'classes': combo.classes.all, 'combo_num': combo.num, 'tot': tot, 'price': price}
    #         return render(request, 'billinglist.html', context)
    # # else:
    # print("not post")
    context = {'name': combo.rider, 'show_date': show.date,
     'classes': combo.classes.all, 'combo_num': combo.num, 'tot': tot, 'price': price}
    return render(request, 'billinglist.html', context)


def scratch(request, showdate, combonum):
    # combonum = request.GET['combonum']
    # showdate = request.GET['showdate']
    # print(combonum+1)
    show = Show.objects.get(date=showdate)
    combo = HorseRiderCombo.objects.get(num=int(combonum))
    cls = request.GET["cname"]
    dcls = combo.classes.get(name=cls)
    # dcls.delete()
    combo.classes.remove(dcls)
    tot = combo.classes.count()
    price = show.preRegistrationPrice * tot
    context = {'name': combo.rider, 'show_date': show.date,
      'classes': combo.classes.all, 'combo_num': combo.num, 'tot': tot, 'price': price}
    return render(request, 'billinglist.html', context)

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

def delete_class(request, divisionname, classname): #deletes a class from a division
    division = Division.objects.get(name=divisionname) #gets the division object from the division name that was passed in
    classObj = Classes.objects.get(name=classname) #gets the class object from the class name that was passed in
    division.classes.remove(classObj) #removes the class object from the division's many-to-many "classes" field
    division.save() #saves the division object in the database
    context = {'classes': division.classes.all,'name': division.name}
    return redirect('division_classes', divisionname=divisionname)  #redirects to division_classes and passes in the division's name



def division_classes(request,divisionname): #lists the classes in a division
    division = Division.objects.get(name= divisionname)  #gets the division object from the division name that was passed in
    context = {'classes': division.classes.all,'name': division.name}
    return render(request, 'division_classes.html', context) #passes the division's name and classes to the "division_classes.html" and renders that page

def new_class(request):
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # return render(request, 'editrider.html', {'form': form})
            return redirect('/show/class')
    else:
        form = ClassForm()
    return render(request, 'new_class.html', {'form': form})


def class_select(request):
    if request.method == "POST":
        form = ClassSelectForm(request.POST)
        if form.is_valid():
            classobj = form.cleaned_data['name']
            classname = classobj.name
            request.session['classobj'] = classname
            return redirect('rankclass', classname)
    else:
        form = ClassSelectForm()
    return render(request, 'class_select.html', {'form': form})


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


class ClassAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Classes.objects.all().order_by('number')
        if self.q:
            qs = qs.filter(class_name__istartswith=self.q)
        return qs


def new_division(request, showname):
    show = Show.objects.get(name=showname)
    date = show.date
    if request.method == "POST":
        if 'exit' in request.POST:
            form = DivisionForm(request.POST)
            if form.is_valid():
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
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                division = Division.objects.get(
                    name=form.cleaned_data['name'])
                divisions = show.divisions
                divisions.add(division)
                show.save()

                return redirect('divisions', showname)
    else:
        form = DivisionForm()
        shows = Show.objects.all().order_by('date')
        for show in shows:
            if showname == show.name:
                context = {
                    "form": form,
                    "name": show.name,
                    "date": show.date,
                    "location": show.location,
                    "divisions": show.divisions.all,
                }
        return render(request, 'new_division.html', context)


def division_select(request, showname): #displays division select dropdown and ability to "Save" or "See Division Scores"
    if request.method == "POST":
        if 'save' in request.POST: #if a division is selected and the "Save" button is clicked
            form = DivisionSelectForm(request.POST)
            if form.is_valid():
                show = Show.objects.get(name=showname) #gets the show object from the showname that was passed in
                current_divisions = show.divisions #gets the divisions of the show object
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
    return render(request, 'division_select.html', {'form': form, 'name': showname}) #passes the DivisionSelectForm and show name to "division_select.html" and renders that page


class DivisionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Division.objects.all().order_by('number')
        if self.q:
            qs = qs.filter(division_name__istartswith=self.q)
        return qs


def select_rider(request):
    if request.method == "POST":
        request.session['rider_pk'] = request.POST['rider']
        return redirect('select_horse')            
    form = RiderSelectForm()
    return render(request, 'rider_select.html', {'form': form})

def add_rider(request):
    if request.method == "POST":
        form = RiderForm(request.POST)
        if form.is_valid():
            rider = form.save()
            request.session['rider_pk'] = rider.pk
            return redirect('select_horse')
    form = RiderForm()
    return render(request, 'editrider.html', {'form': form})

def add_horse(request):
    if request.method == "POST":
        form = HorseForm(request.POST)
        if form.is_valid():
            horse = form.save()
            request.session['horse_pk'] = horse.pk
            return redirect('add_combo')
    form = HorseForm()
    return render(request, 'horse_edit.html', {'form': form})

class RiderAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Rider.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def select_horse(request):
    if request.method == 'POST':
        horse = request.POST['horse']
        request.session['horse_pk'] = request.POST['horse']
        return redirect('add_combo')
    form = HorseSelectForm()
    return render(request, 'horse_select.html', {'form': form})


def add_combo(request):
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
            return redirect('index')
    rider_pk = request.session['rider_pk']
    if rider_pk is None:
        return redirect('index')
    horse_pk = request.session['horse_pk']
    if horse_pk is None:
        return redirect('index')
    rider = get_object_or_404(Rider, pk=rider_pk)
    horse = get_object_or_404(Horse, pk=horse_pk)
    form = HorseRiderComboCreateForm()
    return render(request, 'add_combo.html', {'form': form, 'rider': rider, 'horse': horse})

def edit_combo(request, num):
    combo = HorseRiderCombo.objects.get(pk=num)
    if request.method == "POST":
        form = HorseRiderEditForm(request.POST)
        print(request.POST)
        if form.is_valid():    
            combo.email = form.cleaned_data['email']
            combo.cell = form.cleaned_data['cell']
            combo.contact = form.cleaned_data['contact']
            combo.save()
        else:
            print("INVALID")
    edit_form = HorseRiderEditForm({'email': combo.email, 'cell': combo.cell, 'contact': combo.contact}, instance=combo)
    
    return render(request, 'edit_combo.html', {'combo': combo, 'edit_form': edit_form})

""" def combo(request, num):
    if request.method == "POST":
        combo_form = ComboNumForm(request.POST)
        if combo_form.is_valid():
            combo_num = combo_form.cleaned_data['num']
            try:
                horse_rider_combo = HorseRiderCombo.objects.get(num=combo_num)
                if 'rider_pk' not in request.session and 'horse_pk' not in request.session:
                    rider = horse_rider_combo.rider
                    request.session['rider_pk'] = rider.pk
                    horse = horse_rider_combo.horse
                    request.session['horse_pk'] = horse.pk
                else:
                    rider = Rider.objects.get(pk=request.session['rider_pk'])
                    horse = Horse.objects.get(pk=request.session['horse_pk'])
                num = horse_rider_combo.num
                # request.session['num'] = number
                return render(request, 'check_combo.html', {"num": num, 'rider': rider, 'horse': horse})
            except(HorseRiderCombo.DoesNotExist):
                rider = get_object_or_404(
                    Rider, pk=request.session['rider_pk'])
                horse = get_object_or_404(
                    Horse, pk=request.session['horse_pk'])
                print(rider)
                print(horse)
                horse_rider_combo = HorseRiderCombo.objects.create(
                    num=combo_num, rider=rider, horse=horse)
                return render(request, 'combo.html', {'combo_form': combo_form, 'rider': rider, 'horse': horse})
        else:
            return redirect('showpage', request.session["showdate"])
    return redirect(reverse('index')) """


def check_combo(request, num):
    if request.method == "POST":
        rider = HorseRiderCombo.objects.get(pk=num).rider
        horse = HorseRiderCombo.objects.get(pk=num).horse
        return render(request, 'class_select.html')
    return render(request, 'check_combo.html', {'num': num, 'rider': rider, 'horse': horse})
    # return redirect(reverse('index'))


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

def populate_pdf(request): #populates text fields of PDF
    data_dict = {
        'show': '11/7/2018',
        'judge': 'Bertha',
    } #info to populate the pdf's "show" and "judge" text fields
    write_fillable_pdf("show/static/VHSA_Results_2015.pdf",
                       "show/static/VHSA_Final_Results.pdf", data_dict) #uses "VHSA_Results_2015.pdf" and populates it's fields with the info in data dict, then it saves this new populated pdf to "VHSA_Final_Results.pdf"
    print(os.getcwd())
    return render(request, 'finalresults.html', {"filename": "show/static/VHSA_Final_Results.pdf"}) #returns the populated pdf
