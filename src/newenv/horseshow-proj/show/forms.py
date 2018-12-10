from django import forms
from show.models import *
from .models import *
import datetime
from django.forms import HiddenInput, formset_factory
from dal import autocomplete


#Form for creating a Show and saving its information. This information doesn't get
#edited per Bertha and Rebecca's request as the name, date, and location will be set early on
class ShowForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'autocomplete': 'off', }))
    date = forms.DateField(initial=datetime.date.today)
    location = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off', }))
    dayOfPrice = forms.IntegerField()
    preRegistrationPrice = forms.IntegerField()

#This allows you to check whether they were preregistered, or if they entered certain classes the day of
class RegistrationBillForm(forms.Form):
    typels = ['prereg', 'dayof']
    registrationtype = forms.ChoiceField(choices=typels)

#This allows you to rank classes from 1st through 6th and store those rankings in the specific Class
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

#This allows you to enter information for an individual Rider. Birth date is necessary for people who are 18 or younger
class RiderForm(forms.ModelForm):
    """ Form for a rider with name, address, email, birth date, whether it is a member of the VHSA, and its county """
    birth_date = forms.DateField(help_text="Only enter if you are 18 or younger", widget=forms.SelectDateWidget(
        years=range(1900, 2016)))

    class Meta:
        model = Rider
        fields = ('name', 'address', 'email',
                  'birth_date', 'member_VHSA', 'county',)

#Used to select a rider from the database and prepopulate with options
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

#This form allows you to enter information about an individual Horse.
class HorseForm(forms.ModelForm):
    """ the form for a horse, which has a coggins_date, name, accession number, owner, type, and size """
    coggins_date = forms.DateField(widget=forms.SelectDateWidget(
        years=range(2010, 2019)))

    class Meta:
        model = Horse
        fields = ('name', 'coggins_date', 'accession_no',
                  'owner', 'type', 'size', )

#This form allows you to select a combo
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

#This combo Num Form is used to give each horse and rider a unique combo number
class ComboNumForm(forms.Form):
    """ the form for entering a horse rider combo number to go to its edit page """
    # class Meta:
    #     model = HorseRiderCombo
    #     fields = ('num',)
    num = forms.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)])

#This creates the Horse Rider Combo itself
class HorseRiderComboCreateForm(forms.ModelForm):
    """ for creating a horse rider combo """
    class Meta:
        model = HorseRiderCombo
        fields = ('num', 'contact', 'email', 'cell')

#This allows you to edit the HorseRiderCombo's infromation. The combo number cannot be changed.
class HorseRiderEditForm(forms.ModelForm):
    """ for updating a horse-rider combo """
    class Meta:
        model = HorseRiderCombo
        fields = ('contact', 'email', 'cell')

#This allows you to edit the rider's information
class RiderEditForm(forms.ModelForm):
    """ for updating a rider """
    class Meta:
        model = Rider
        fields = ('name', 'address', 'birth_date', 'member_VHSA', 'county')

#This allows you to edit the horse's information
class HorseEditForm(forms.ModelForm):
    """ for editing a horse """
    class Meta:
        model = Horse
        fields = ('accession_no', 'coggins_date',
                  'owner', 'type', 'size')

#This allows you to select a show from a prepopulated list that you can search from
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

#This allows you to select a horse from a prepopulated list that you can also search from
class HorseSelectForm(forms.ModelForm):
    horse = forms.ModelChoiceField(
        queryset=Horse.objects.all(),
        widget=autocomplete.ModelSelect2(url='horse_autocomplete')
    )  # form with horse autocomplete dropdown

    class Meta:
        model = Horse
        fields = ('horse',)


#This form allows you to enter class information for a show

class AddClassForm(forms.Form):
    #create a new class
    class Meta:
        model = Classes
        fields = ('name', 'number',)

#This form is a model form for Classes.
class ClassForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ('name', 'number')


#This is another class form
class AddClassForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ('name', 'number')


#This allows the user to remove classes by entering the class number
class RemoveClassForm(forms.Form):
    num = models.IntegerField()

#This form allows the user to select a class from a prepopulated menu
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

#This form allows info to be entered for a division
class DivisionForm(forms.ModelForm):
    #create new division
    class Meta:
        model = Division
        fields = ('name', 'number')

#This form provides information for the division champion of a specific division, recording the
#champion/champion reserve and their respective points
class DivisionChampForm(forms.ModelForm):
    class Meta:
        model = Division

        fields = ('champion', 'champion_pts',
                  'champion_reserve', 'champion_reserve_pts')

#This form allows the user to select a division from a prepopulated form
class DivisionSelectForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        widget=autocomplete.ModelSelect2(url='division_autocomplete')
    )

    class Meta:
        model = Division
        fields = ('name',)
