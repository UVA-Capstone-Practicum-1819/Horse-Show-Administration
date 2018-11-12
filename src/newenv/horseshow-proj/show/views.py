import random
import os
import json
import pdfrw
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import resolve, reverse
from show.forms import ShowForm, RiderForm, HorseForm, HorseSelectForm, ClassForm, DivisionForm, ShowSelectForm, RiderSelectForm, ComboForm, ClassSelectForm, DivisionSelectForm
from django.forms.models import model_to_dict
from show.models import Show, Rider, Horse, Classes, Division
from django.utils import timezone
from dal import autocomplete
""" for authentication/signin/signup purposes """
from .populatepdf import write_fillable_pdf
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


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
    latest_show_list = Show.objects.all
    template = loader.get_template('index.html')
    context = {
        'latest_show_list': latest_show_list,
    }
    return HttpResponse(template.render(context, request))


def showpage(request):
    latest_show_list = Show.objects.all
    template = loader.get_template('showpage.html')
    context = {
        'latest_show_list': latest_show_list,
    }
    return HttpResponse(template.render(context, request))


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
    showname = f.cleaned_data['show_name']
    showdate = f.cleaned_data['show_date']
    showlocation = f.cleaned_data['show_location']
    #get_shows = Show.objects.all()
    # all_shows = [show for show in get_shows]
    # failure = False
    # for show in all_shows:
    #     if showname == show.object.get(show_name = showname) and showdate == show['show_date'] and showlocation == show['show_location']:
    #         failure = True
    # if failure:
    #     response = {'ok': False, 'error_msg': "This show has already been created!", 'form': form}
    #     return render(request, 'create_show.html', response)
    new_show = Show.objects.create(
        show_name=showname, show_date=showdate, show_location=showlocation)
    response = {'ok': True, 'success_msg': "Show was successfully created",
                'form': form, 'show': new_show}
    return render(request, 'create_show.html', response)


def show_select(request):
    if request.method == "POST":
        form = ShowSelectForm(request.POST)
        if form.is_valid():
            #post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            # post.save()
            # return redirect('horse_detail', pk=post.pk)
            return redirect('viewshow', showname=form.cleaned_data['name'])
    else:
        form = ShowSelectForm()
    return render(request, 'show_select.html', {'form': form})


class ShowAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
            # return Horse.objects.none()
        qs = Show.objects.all()
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

def viewshow(request, showname):
    try:
        # find the show to be viewed
        # store data in context to be accessible by html page
        shows = Show.objects.all()
        for show in shows:
            if showname == show.show_name:
                context = {
                    "show_name" : show.show_name,
                    "show_date" : show.show_date,
                    "show_location" : show.show_location,
                }
                return render(request, 'viewshow.html', context = context)
    except Exception as e:
        return HttpResponse(e)

def edit_show(request, showname):
    return render(request,"edit_show.html")

def billing(request):
    if request.method == "POST":
        form = RiderSelectForm(request.POST)
        if form.is_valid():
            #post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            # post.save()
            # return redirect('horse_detail', pk=post.pk)
            return render(request, 'billing.html', {'form': form})
    else:
        form = RiderSelectForm()
    return render(request, 'billing.html', {'form': form})

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
            # return render(request, 'horse_select.html', {'form': form})
            return redirect('/show/')
    else:
        form = ClassSelectForm()
    return render(request, 'class_select.html', {'form': form})

class ClassAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Classes.objects.all()
        if self.q:
            qs = qs.filter(class_name__istartswith=self.q)
        return qs

def new_division(request):
    if request.method == "POST":
        form = DivisionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('/show/division')
    else:
        form = DivisionForm()
    return render(request, 'new_division.html', {'form': form})

def division_select(request):
    if request.method == "POST":
        form = DivisionSelectForm(request.POST)
        if form.is_valid():
            # return render(request, 'horse_select.html', {'form': form})
            return redirect('/show/')
    else:
        form = DivisionSelectForm()
    return render(request, 'division_select.html', {'form': form})

class DivisionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Division.objects.all()
        if self.q:
            qs = qs.filter(division_name__istartswith=self.q)
        return qs

def newrider(request):
    print(request.method)
    if request.method == "POST":
        form = RiderForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # return render(request, 'editrider.html', {'form': form})
            return redirect('/show/horse')
    else:
        form = RiderForm()
    return render(request, 'editrider.html', {'form': form})


def rider_select(request):
    if request.method == "POST":
        form = RiderSelectForm(request.POST)
        if form.is_valid():
            # return render(request, 'horse_select.html', {'form': form})
            return redirect('/show/horse')
    else:
        form = RiderSelectForm()
    return render(request, 'rider_select.html', {'form': form})


class RiderAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Rider.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def horse_select(request):
    if request.method == "POST":
        form = HorseSelectForm(request.POST)
        if form.is_valid():
            #post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            # post.save()
            # return redirect('horse_detail', pk=post.pk)
            return render(request, 'horse_select.html', {'form': form})
    else:

        form = HorseSelectForm()
    return render(request, 'horse_select.html', {'form': form})


def horse_new(request):
    print(request.method)
    if request.method == "POST":
        form = HorseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # return redirect('horse_detail', pk=post.pk)
            return render(request, 'horse_edit.html', {'form': form})
    else:
        form = HorseForm()
    return render(request, 'horse_edit.html', {'form': form})


class HorseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        # if not self.request.user.is_authenticated():
            # return Horse.objects.none()

        qs = Horse.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


# def add_combo(request):
#     form = ComboForm()
#     if request.method == "GET":
#         return render(request, 'add_combo.html', {'form': form})
#     f = Combo(request.POST)
#     if not f.is_valid():
#         return render(request, 'add_combo.html', {'form': f})
#     if f.is_valid():
#         post = form.save(commit=False)
#         post.author = request.user
#         post.published_date = timezone.now()
#         post.save()
#         return render(request, 'add_combo.html', {'form': f})
#     combo = random.randint(100, 999)
#     ridername = f.cleaned_data['rider_name']
#     horsename = f.cleaned_data['horse_name']
#     owner = f.cleaned_data['owner']

#     new_combo = Combo.objects.create(
#         combo=combo, rider_name=ridername, horse_name=horsename, owner=owner)
#     response = {'ok': True, 'success_msg': "Horse rider combination was successfully created",
#                 'form': form, 'combo': combo}
#     return render(request, 'add_combo.html', response)

def add_combo(request, rider_name, horse_name):
    rider = get_object_or_404(Rider, pk=rider_name)
    try:
        selected_rider = rider.choice_set.get(pk=request.POST['rider name'])
    except (KeyError, Choice.DoesNotExist):
        # Add a rider to the database
        return render(request, 'rider/new.html', {
            'error_message': "Rider do not exist in database, add a new rider",
        })
    else:
        selected_rider.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def new_class(request):
    print(request.method)
    if request.method == "POST":
        form = ClassesForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # return redirect('horse_detail', pk=post.pk)
            return render(request, 'classes.html', {'form': form})
    else:
        form = ClassesForm()
    return render(request, 'classes.html', {'form': form})

def populate_pdf(request):
     data_dict = {
                'show': '11/7/2018',
                'judge': 'Bertha',
                }
     write_fillable_pdf("show/static/VHSA_Results_2015.pdf", "show/static/VHSA_Final_Results.pdf", data_dict)
     print(os.getcwd())
     return render(request, 'finalresults.html',{"filename":"show/static/VHSA_Final_Results.pdf"})
