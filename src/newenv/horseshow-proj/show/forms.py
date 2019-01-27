from django import forms
from show.models import *
from .models import *
import datetime
from django.forms import HiddenInput, formset_factory
from dal import autocomplete


class ShowForm(forms.Form):
    """ 
    Form for creating a Show and saving its information. This information doesn't get edited per Bertha and Rebecca's request as the name, date, and location will be set early on 
    """
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'autocomplete': 'off', }))
    date = forms.DateField(initial=datetime.date.today)
    location = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off', }))
    day_of_price = forms.IntegerField(label="Day-of Price")
    pre_reg_price = forms.IntegerField(label="Preregistration Price")


class RegistrationBillForm(forms.Form):
    """ 
    This allows you to check whether they were preregistered, or if they entered certain classes the day of 
    """
    types = ['pre_reg', 'day_of']
    registrationtype = forms.ChoiceField(choices=types)


class RankingForm(forms.Form):
    """ 
    This allows you to rank classes from 1st through 6th and store those rankings in the specific Class 
    """
    first = forms.IntegerField()
    second = forms.IntegerField()
    third = forms.IntegerField()
    fourth = forms.IntegerField()
    fifth = forms.IntegerField()
    sixth = forms.IntegerField()

    fields = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']


class RiderForm(forms.ModelForm):
    """ 
    This allows you to enter information for an individual Rider. Birth date is necessary for people who are 18 or younger. Form for a rider with name, address, email, birth date, whether it is a member of the VHSA, and its county 
    """
    birth_date = forms.DateField(help_text="Only enter if you are 18 or younger", widget=forms.SelectDateWidget(
        years=range(1900, 2016)))

    class Meta:
        model = Rider
        fields = ('name', 'address', 'email',
                  'birth_date', 'member_VHSA', 'county',)


class RiderSelectForm(forms.ModelForm):
    """ 
    Form for selecting a rider and returning its primary key. Used to select a rider from the database and prepopulate with options
    """

    rider = forms.ModelChoiceField(
        queryset=Rider.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='rider_autocomplete')
    )

    class Meta:
        model = Rider
        fields = ('rider',)


class HorseForm(forms.ModelForm):
    """ 
    This form allows you to enter information about an individual Horse. The form for a horse, which has a coggins_date, name, accession number, owner, type, and size 
    """
    coggins_date = forms.DateField(widget=forms.SelectDateWidget(
        years=range(2010, 2019)))

    class Meta:
        model = Horse
        fields = ('name', 'coggins_date', 'accession_num',
                  'owner', 'type', 'size', )


class ComboSelectForm(forms.ModelForm):
    """ This form allows you to select a combo. returns the primary key of the horse rider combo in a drop down list """
    combo = forms.ModelChoiceField(
        queryset=HorseRiderCombo.objects.all(),
        widget=autocomplete.ModelSelect2(url='combo_autocomplete')
    )

    class Meta:
        model = HorseRiderCombo
        fields = ('combo',)


class ComboNumForm(forms.Form):
    """ # This combo Num Form is used to give each horse and rider a unique combo number. The form for entering a horse rider combo number to go to its edit page """
    # class Meta:
    #     model = HorseRiderCombo
    #     fields = ('num',)
    num = forms.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)])


class HorseRiderComboCreateForm(forms.ModelForm):
    """ # This creates the Horse Rider Combo itself. for creating a horse rider combo """
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
        fields = ('accession_num', 'coggins_date',
                  'owner', 'type', 'size')


class ShowSelectForm(forms.ModelForm):

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


class HorseSelectForm(forms.ModelForm):
    horse = forms.ModelChoiceField(
        queryset=Horse.objects.all(),
        widget=autocomplete.ModelSelect2(url='horse_autocomplete')
    )  # form with horse autocomplete dropdown

    class Meta:
        model = Horse
        fields = ('horse',)


class ClassForm(forms.ModelForm):
    """ # This form is a model form for Class. """
    class Meta:
        model = Class
        fields = ('num', )


class RemoveClassForm(forms.Form):
    """ # This allows the user to remove classes by entering the class number """
    num = models.IntegerField()


class ClassSelectForm(forms.ModelForm):
    """ # This form allows the user to select a class from a prepopulated menu """
    selected_class = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='classes_autocomplete'),
    )

    class Meta:
        model = Class
        fields = ('selected_class',)

    def clean_date(self):
        class_obj = self.cleaned_data['name']
        classes = Class.objects.all()
        if class_obj in classes:
            class_obj.name = class_obj.name
            return class_obj


class DivisionForm(forms.ModelForm):
    """ # This form allows info to be entered for a division """

    class Meta:
        model = Division
        fields = ('name', )


class DivisionChampForm(forms.ModelForm):
    """ 
    This form provides information for the division champion of a specific division, recording the champion/champion reserve and their respective points 
    """
    class Meta:
        model = Division

        fields = ('champion', 'champion_pts',
                  'champion_reserve', 'champion_reserve_pts')


class DivisionSelectForm(forms.ModelForm):
    """ This form allows the user to select a division from a prepopulated form """
    name = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        widget=autocomplete.ModelSelect2(url='division_autocomplete')
    )

    class Meta:
        model = Division
        fields = ('name',)
