from django import forms
from show.models import *
from .models import *
import datetime
from django.forms import HiddenInput, formset_factory
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
    first = forms.IntegerField()
    second = forms.IntegerField()
    third = forms.IntegerField()
    fourth = forms.IntegerField()
    fifth = forms.IntegerField()
    sixth = forms.IntegerField()

    class Meta:
        model = Classes
        fields = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']


class RiderForm(forms.ModelForm):
    """ Form for a rider with name, address, email, birth date, whether it is a member of the VHSA, and its county """
    birth_date = forms.DateField(help_text="Only enter if you are 18 or younger", widget=forms.SelectDateWidget(
        years=range(1900, 2016)))

    class Meta:
        model = Rider
        fields = ('name', 'address', 'email',
                  'birth_date', 'member_VHSA', 'county',)


class RiderSelectForm(forms.ModelForm):
    """ Form for selecting a rider and returning its primary key """
    # horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))
    # rider_names =  [rider.name for rider in Rider.objects.all()]
    rider = forms.ModelChoiceField(
        queryset=Rider.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='rider_autocomplete')
    )

    class Meta:
        model = Rider
        fields = ('rider',)


class HorseForm(forms.ModelForm):
    """ the form for a horse, which has a coggins_date, name, accession number, owner, type, and size """
    coggins_date = forms.DateField(widget=forms.SelectDateWidget(
        years=range(2010, 2019)))

    class Meta:
        model = Horse
        fields = ('name', 'coggins_date', 'accession_no',
                  'owner', 'type', 'size', )


class ComboSelectForm(forms.ModelForm):
    """ returns the primary key of the horse rider combo in a drop down list """
    # horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))
    # rider_names =  [rider.name for rider in Rider.objects.all()]
    combo = forms.ModelChoiceField(
        queryset=HorseRiderCombo.objects.all(),
        widget=autocomplete.ModelSelect2(url='combo_autocomplete')
    )

    class Meta:
        model = HorseRiderCombo
        fields = ('combo',)


class ComboNumForm(forms.Form):
    """ the form for entering a horse rider combo number to go to its edit page """
    # class Meta:
    #     model = HorseRiderCombo
    #     fields = ('num',)
    num = forms.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)])


class HorseRiderComboCreateForm(forms.ModelForm):
    """ for creating a horse rider combo """
    class Meta:
        model = HorseRiderCombo
        fields = ('num', 'contact', 'email', 'cell')


class HorseRiderEditForm(forms.ModelForm):
    """ for updating a horse-rider combo """
    class Meta:
        model = HorseRiderCombo
        fields = ('contact', 'email', 'cell')


class RiderEditForm(forms.ModelForm):
    """ for updating a rider """
    class Meta:
        model = Rider
        fields = ('name', 'address', 'birth_date', 'member_VHSA', 'county')


class HorseEditForm(forms.ModelForm):
    """ for editing a horse """
    class Meta:
        model = Horse
        fields = ('accession_no', 'coggins_date',
                  'owner', 'type', 'size')


class ShowSelectForm(forms.ModelForm):
    # horses = forms.ModelChoiceField(queryset=Horse.objects.all().order_by('name'))

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
    horse = forms.ModelChoiceField(
        queryset=Horse.objects.all(),
        widget=autocomplete.ModelSelect2(url='horse_autocomplete')
    )  # form with horse autocomplete dropdown

    class Meta:
        model = Horse
        fields = ('horse',)


class AddClassForm(forms.Form):
    class Meta:
        model = Classes
        fields = ('name', 'number')


class ClassForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ('name', 'number')


class AddClassForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ('name', 'number')


class RemoveClassForm(forms.Form):
    num = models.IntegerField()


class ClassSelectForm(forms.ModelForm):
    selected_class = forms.ModelChoiceField(
        queryset=Classes.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='classes_autocomplete'),
    )

    class Meta:
        model = Classes
        fields = ('selected_class',)

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

        fields = ('champion', 'champion_pts',
                  'champion_reserve', 'champion_reserve_pts')


class DivisionSelectForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        widget=autocomplete.ModelSelect2(url='division_autocomplete')
    )

    class Meta:
        model = Division
        fields = ('name',)
