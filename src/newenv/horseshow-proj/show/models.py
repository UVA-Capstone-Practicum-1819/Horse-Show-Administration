from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator, RegexValidator
import random
import datetime

#Model for a Show, includes basic information such as name/date/location and a pre_reg_price
#for riders who sign up for classes early. There is a dayof price for riders who sign up the day of the show.
class Show(models.Model):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100, primary_key=True)
    location = models.CharField(max_length=100)
    day_of_price = models.IntegerField(blank=True, null=True, default=0, verbose_name="Day-of Price")
    pre_reg_price = models.IntegerField(blank=True, null=True, default=0, verbose_name="Preregistration Price")
    def __str__(self):
        return self.date

#Model for a single division. Includes a name, number for the division, and a
# champion and champion reserve for the division as well as the points they earned in that division
class Division(models.Model):
    name = models.CharField(primary_key=True, max_length=100, default="")
    champion = models.IntegerField(default=0)
    champion_pts = models.IntegerField(default=0)
    champion_reserve = models.IntegerField(default=0)
    champion_reserve_pts = models.IntegerField(default=0)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="divisions")
    def __str__(self):
        return self.name

#Model for a single class. Because class is recognized in coding, we changed the name of a
#single class to classes. Includes rankings from 1st through 6th and a number for the class as
#well as a name
class Class(models.Model):
    number = models.IntegerField(default=0)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name="classes")
    def __str__(self):
        return str(self.number)

#Model for a horse, includes possible sizes of the horse and the choice to refer to it as a horse or a Pony
#coggins date is important for health consideration and the owner is not necessarily the riders
class Horse(models.Model):
    alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    size_choices = ( ("NA", "N/A"), ("small", "SM"), ("medium", "MED"), ("large", "LG"), )
    type_choices = ( ("horse", "Horse"), ("pony", "Pony"), )
    name = models.CharField(primary_key=True, max_length=200, verbose_name="Name (Barn Name)")
    accession_no = models.CharField(max_length=200, verbose_name="Accession Number", validators=[alphanumeric_validator])
    coggins_date = models.DateField(default=datetime.date.today,  verbose_name="Coggins Date", )
    owner = models.CharField(max_length=200, verbose_name="Owner")
    type = models.CharField(max_length=200, choices=type_choices, default="Horse", verbose_name="Type")
    size = models.CharField(max_length=200, choices=size_choices, default="N/A", verbose_name="Size")
    def __str__(self):
        return self.name

#Model for a rider. Birth date only needs to be recorded if they are 18 or younger
class Rider (models.Model):
    email = models.EmailField(primary_key=True, max_length=200, validators=[EmailValidator()], verbose_name="Email")
    name = models.CharField(max_length=200, verbose_name="Name")
    address = models.CharField(max_length=200, verbose_name="Address")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Birth Date", )
    member_VHSA = models.BooleanField(default=False, blank=True, verbose_name="Member of the VHSA")
    county = models.CharField(max_length=200, blank=True, verbose_name="If member of 4H, specify county")
    horses = models.ManyToManyField(Horse, through='HorseRiderCombo')
    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}"



#Model that contains information about the Horse Rider Combo. Used to describe the
#relationship between a specific horse and specific rider for the day of the show
#Class scores are recorded for each class they compete in
class HorseRiderCombo(models.Model):
    num = models.IntegerField(primary_key=True, validators=[MinValueValidator(100), MaxValueValidator(999)], verbose_name="Combination Number")

    contact_choices = ( ("rider", "Rider"), ("owner", "Owner"),
        ("parent", "Parent"), ("trainer", "Trainer") )
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, verbose_name="Rider")
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, verbose_name="Horse")
    classes = models.ManyToManyField(Class, verbose_name="Classes", blank=True, through='ClassParticipation', related_name="combos")
    contact = models.CharField(max_length=100, choices=contact_choices, default="rider", verbose_name="Contact")
    email = models.EmailField(blank=True, null=True, verbose_name="Contact Email")
    cell = models.CharField(max_length=12, blank=True, verbose_name="Contact Cell Phone Number")
    def __str__(self):
        return str(self.num)

#Model for a ClassParticipation. Includes a participating class and a score for that class to be placed under a HorseRider Combo
class ClassParticipation(models.Model):
    participated_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    
    combo = models.ForeignKey(HorseRiderCombo, verbose_name="Horse Rider Combo", on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    is_preregistered = models.BooleanField(default=False)
    def __str__(self):
        return f"Combo #{self.combo.num} participates in class {self.participated_class.number}"