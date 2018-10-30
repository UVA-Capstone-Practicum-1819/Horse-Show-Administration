
# Create your views here.
import random
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import resolve, reverse
import json
from show.forms import ShowForm, RiderForm, HorseForm, HorseSelectForm, ClassesForm, ShowSelectForm, RiderSelectForm, ComboForm
from django.forms.models import model_to_dict
from show.models import Show, Rider, Horse, Combo
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from dal import autocomplete

# Create your views here.

""" for authentication/signin/signup purposes """
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
            return render(request, 'show_select.html', {'form': form})
    else:
        form = ShowSelectForm()
    return render(request, 'show_select.html', {'form': form})


class ShowAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
            # return Horse.objects.none()
        qs = Show.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
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


def add_combo(request):
    form = ComboForm()
    if request.method == "GET":
        return render(request, 'add_combo.html', {'form': form})
    f = Combo(request.POST)
    if not f.is_valid():
        return render(request, 'add_combo.html', {'form': f})
    if f.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        post.save()
        return render(request, 'add_combo.html', {'form': f})
    combo = random.randint(100, 999)
    ridername = f.cleaned_data['rider_name']
    horsename = f.cleaned_data['horse_name']
    owner = f.cleaned_data['owner']

    new_combo = Combo.objects.create(
        combo=combo, rider_name=ridername, horse_name=horsename, owner=owner)
    response = {'ok': True, 'success_msg': "Horse rider combination was successfully created",
                'form': form, 'combo': combo}
    return render(request, 'add_combo.html', response)


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
