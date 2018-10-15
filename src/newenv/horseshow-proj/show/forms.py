from django import forms
from show import views
from show.models import *
from .models import *


class ShowForm(forms.Form):
    show_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    show_date = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    show_location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))

class RiderForm(forms.ModelForm):
    class Meta:
        model = Rider
        fields = ('name', 'address', 'age', 'email')

class Horse(forms.ModelForm):

    class Meta:
        model = Horse
        fields = ('name', 'barn_name', 'age', 'coggins','owner', 'size', 'type')
