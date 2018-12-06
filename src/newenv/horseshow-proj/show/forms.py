from django import forms
from show.models import *
from .models import *
import datetime
from django.forms import HiddenInput
from dal import autocomplete


class ShowForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'autocomplete': 'off', }))
    date = forms.DateField(initial=datetime.date.today)
    location = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off', }))
    dayOfPrice = forms.IntegerField()
    preRegistrationPrice = forms.IntegerField()


class RegistrationBillForm(forms.Form):
    typels = ['prereg', 'dayof']
    registrationtype = forms.ChoiceField(choices=typels)


class RankingForm(forms.ModelForm):
    first=forms.IntegerField()
    second=forms.IntegerField()
    third=forms.IntegerField()
    fourth=forms.IntegerField()
    fifth=forms.IntegerField()
    sixth=forms.IntegerField()

    class Meta:
        model = Classes
        fields = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']



class RiderForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Name', 'required': True, }))
    address = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Address', 'required': True, }))
    age = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': 'Age', 'required': True, }))
    email = forms.CharField(max_length=100, widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'required': True, }))

    class Meta:
        model = Rider
        fields = ('name', 'address', 'age', 'email')


class RiderSelectForm(forms.ModelForm):
    #horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))
        # rider_names =  [rider.name for rider in Rider.objects.all()]
    rider = forms.ModelChoiceField(
        queryset=Rider.objects.all(),
        widget=autocomplete.ModelSelect2(url='rider_autocomplete')
    )

    class Meta:
        model = Rider
        fields = ('rider',)


class HorseForm(forms.ModelForm):
    class Meta:
        model = Horse
        fields = ('name', 'barn_name', 'age',
                  'coggins', 'owner', 'size', 'type')


class ComboSelectForm(forms.ModelForm):
    #horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))
        # rider_names =  [rider.name for rider in Rider.objects.all()]
    combo = forms.ModelChoiceField(
        queryset=HorseRiderCombo.objects.all(),
        widget=autocomplete.ModelSelect2(url='combo_autocomplete')
    )

    class Meta:
        model = HorseRiderCombo
        fields = ('combo',)


class ComboForm(forms.ModelForm):
    class Meta:
        model = HorseRiderCombo
        fields = ('num', 'rider', 'horse')


class ComboNumForm(forms.Form):
    # class Meta:
    #     model = HorseRiderCombo
    #     fields = ('num',)
    num = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)])


class ShowSelectForm(forms.ModelForm):
    #horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))

    date = forms.ModelChoiceField(
        queryset=Show.objects.all(),
        widget=autocomplete.ModelSelect2(url='show_autocomplete')
    )

    class Meta:
        model = Show
        fields = ('date',)

    def clean_date(self):
        showobj = self.cleaned_data['date']
        shows = Show.objects.all()
        if showobj in shows:
            showobj.date = showobj.date + 'foo'
            return showobj

    # def clean(self):

        # widgets = {
        #    'name': autocomplete.ModelSelect2(nk
        #    url='horse-autocomplete',
        #    attrs={'data-html': True}
        #    )
        #    }


class HorseSelectForm(forms.ModelForm):
    #horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))
    horse = forms.ModelChoiceField(
        queryset=Horse.objects.all(),
        widget=autocomplete.ModelSelect2(url='horse_autocomplete')
    )

    class Meta:
        model = Horse
        fields = ('horse',)
        # widgets = {
        #    'name': autocomplete.ModelSelect2(
        #    url='horse-autocomplete',
        #    attrs={'data-html': True}
        #    )
        #    }


class ClassForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ('name', 'number')


class ClassSelectForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Classes.objects.all(),
        widget=autocomplete.ModelSelect2(url='classes_autocomplete')
    )

    class Meta:
        model = Classes
        fields = ('name',)

    def clean_date(self):
        classobj = self.cleaned_data['name']
        classes = Classes.objects.all()
        if classobj in classes:
            classobj.name = classobj.name
            return classobj


class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ('name', 'number')

class DivisionChampForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ('champion', 'champion_pts', 'champion_reserve', 'champion_reserve_pts')
        
class DivisionSelectForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        widget=autocomplete.ModelSelect2(url='division_autocomplete')
    )

    class Meta:
        model = Division
        fields = ('name',)
