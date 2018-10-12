# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import json
import show.forms
from django.forms.models import model_to_dict
from show.models import Show



def index(request):
    latest_show_list = Show.objects.order_by(show_name)
    template = loader.get_template('show/index.html')
    context = {
        'latest_show_list': latest_show_list,
    }
    return HttpResponse(template.render(context, request))


def create_show(request):
    form = show.forms.ShowForm()
    if request.method == "GET":
        return render(request, 'create_show.html', {'form': form})
    f = show.forms.ShowForm(request.POST)
    if not f.is_valid():
        return render(request, 'create_show.html', {'form': f})
    showname = f.cleaned_data['show_name']
    showdate = f.cleaned_data['show_date']
    showlocation = f.cleaned_data['show_location']
    get_shows = Show.objects.all()
    all_shows = [show.as_json() for show in get_shows]
    failure = False
    for show in all_shows:
        if showname == show['show_name'] and showdate == show['show_date'] and showlocation == show['show_location']:
            failure = True
    if failure:
        response = {'ok': False, 'error_msg': "This show has already been created!", 'form': form}
        return render(request, 'create_show.html', response)
    new_show = Show.objects.create(show_name=showname, show_date=showdate, show_location=showlocation)
    response = {'ok': True, 'success_msg': "Show was successfully created", 'form': form, 'show': new_show.as_json()}
    return render(request, 'create_show.html', response)
