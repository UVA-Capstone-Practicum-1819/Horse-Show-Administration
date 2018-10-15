from django import forms
from show import views
from show.models import *


class ShowForm(forms.Form):
    show_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    show_date = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    show_location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
