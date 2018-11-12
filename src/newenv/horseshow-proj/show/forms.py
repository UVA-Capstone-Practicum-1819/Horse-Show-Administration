from django import forms
from show.models import *
from .models import *
from dal import autocomplete

class ShowForm(forms.Form):
    show_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    show_date = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    show_location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))

class RiderForm(forms.ModelForm):
    class Meta:
        model = Rider
        fields = ('name', 'address', 'age', 'email')

class RiderSelectForm(forms.ModelForm):
    #horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))
    name= forms.ModelChoiceField(queryset=Rider.objects.all(), widget=autocomplete.ModelSelect2(url='rider_autocomplete'))
    class Meta:
        model = Rider
        fields = ('name',)

class HorseForm(forms.ModelForm):
    class Meta:
        model = Horse
        fields = ('name', 'barn_name', 'age', 'coggins','owner', 'size', 'type')

class ComboForm(forms.Form):
    combo = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    rider_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    horse_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))
    owner = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off',}))

class ShowSelectForm(forms.ModelForm):
    #horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))
    name= forms.ModelChoiceField(
        queryset=Show.objects.all(),
        widget=autocomplete.ModelSelect2(url='show_autocomplete')
    )
    class Meta:
        model = Show
        fields = ('name', 'show_date')
        #widgets = {
        #    'name': autocomplete.ModelSelect2(
            #    url='horse-autocomplete',
            #    attrs={'data-html': True}
        #    )
        #    }

class HorseSelectForm(forms.ModelForm):
    #horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))
    name = forms.ModelChoiceField(
        queryset=Horse.objects.all(),
        widget=autocomplete.ModelSelect2(url='horse_autocomplete')
    )
    class Meta:
        model = Horse
        fields = ('name',)
        #widgets = {
        #    'name': autocomplete.ModelSelect2(
            #    url='horse-autocomplete',
            #    attrs={'data-html': True}
        #    )
        #    }
class ClassForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ('class_name', 'class_number')

class ClassSelectForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Classes.objects.all(),
        widget=autocomplete.ModelSelect2(url='classes_autocomplete')
    )
    class Meta:
        model = Classes
        fields = ('name',)

class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ('division_name', 'division_number')

class DivisionSelectForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        widget=autocomplete.ModelSelect2(url='division_autocomplete')
    )
    class Meta:
        model = Division
        fields = ('name',)