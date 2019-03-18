from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator, RegexValidator
import random
import datetime

from localflavor.us.models import USStateField, USZipCodeField

from django.core.exceptions import ValidationError


class Show(models.Model):
    """
    Model for a Show, includes basic information such as name/date/location and a pre_reg_price
    for riders who sign up for classes early. There is a dayof price for riders who sign up the day of the show.
    """
    date = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    day_of_price = models.IntegerField(
        blank=True, null=True, default=0, verbose_name="Day-of Price")
    pre_reg_price = models.IntegerField(
        blank=True, null=True, default=0, verbose_name="Preregistration Price")

    def __str__(self):
        return str(self.date)


class Division(models.Model):
    """
    Model for a single division. Includes a name, number for the division, and a champion and champion reserve for the division as well as the points they earned in that division
    """
    class Meta:
        unique_together = ('show', 'name')
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    champion = models.IntegerField(default=0)
    champion_pts = models.IntegerField(default=0)
    champion_reserve = models.IntegerField(default=0)
    champion_reserve_pts = models.IntegerField(default=0)
    show = models.ForeignKey(
        Show, on_delete=models.CASCADE, related_name="divisions", null=True)

    def __str__(self):
        return f"Show: {self.show.date}, Division: {self.name}"


class Class(models.Model):
    """
    Model for a single class. Because class is recognized in coding, we changed the name of a
    """
    class Meta:
        unique_together = ('show', 'num')
        ordering = ('num',)

    num = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="")
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="classes", null=True)
    show = models.ForeignKey(
        Show, on_delete=models.CASCADE, related_name="classes", null=True)
    first = models.IntegerField(blank=True, null=True)
    second = models.IntegerField(blank=True, null=True)
    third = models.IntegerField(blank=True, null=True)
    fourth = models.IntegerField(blank=True, null=True)
    fifth = models.IntegerField(blank=True, null=True)
    sixth = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.num) + ". " + self.name


class Horse(models.Model):
    """
    Model for a horse, includes possible sizes of the horse and the choice to refer to it as a horse or a Pony coggins date is important for health consideration and the owner is not necessarily the riders
    """
    alphanumeric_validator = RegexValidator(
        r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    size_choices = (("NA", "N/A"), ("small", "SM"),
                    ("medium", "MED"), ("large", "LG"), )
    type_choices = (("horse", "Horse"), ("pony", "Pony"), )
    name = models.CharField(primary_key=True, max_length=200,
                            verbose_name="Name (Barn Name)")
    accession_num = models.CharField(
        max_length=20, verbose_name="Accession Number", validators=[alphanumeric_validator])
    coggins_date = models.DateField(
        default=datetime.date.today,  verbose_name="Coggins Date", )
    owner = models.CharField(max_length=200, verbose_name="Owner")
    type = models.CharField(
        max_length=200, choices=type_choices, default="Horse", verbose_name="Type")
    size = models.CharField(max_length=200, choices=size_choices,
                            default="N/A", verbose_name="Size (if pony)")

    def __str__(self):
        return self.name


class Rider(models.Model):
    """ Model for a rider. Birth date only needs to be recorded if they are 18 or younger. Street address and city are not required """
    class Meta:
        unique_together = ('first_name', 'last_name', 'email')

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, validators=[
        EmailValidator()], verbose_name="Email")

    address = models.CharField(
        max_length=200, verbose_name="Street Address", blank=True)
    city = models.CharField(default="", max_length=200, blank=True)
    state = USStateField(default="VA")
    zip_code = USZipCodeField()
    adult = models.BooleanField(
        default=False, verbose_name="Adult")
    birth_date = models.DateField(
        blank=True, null=True, verbose_name="Birth Date", )
    member_VHSA = models.BooleanField(
        default=False, blank=True, verbose_name="Member of the VHSA")
    member_4H = models.BooleanField(
        default=False, blank=True, verbose_name="Member of the 4H")
    county = models.CharField(max_length=100, default="", blank=True,
                              help_text="Only need to specify this if you are a 4H member")
    horses = models.ManyToManyField(Horse, through='HorseRiderCombo')

    def __str__(self):
        return f"{self.last_name}, {self.first_name}, Email: {self.email}"


class HorseRiderCombo(models.Model):
    """
    Model that contains information about the HRC. Used to describe the
    relationship between a specific horse and specific rider for the day of the show
    Class scores are recorded for each class they compete in
    """
    class Meta:
        unique_together = (('rider', 'horse', 'show'), ('num', 'show'))

    num = models.IntegerField(validators=[MinValueValidator(
        100), MaxValueValidator(999)], verbose_name="Combination Number")

    contact_choices = (("rider", "Rider"), ("owner", "Owner"),
                       ("parent", "Parent"), ("trainer", "Trainer"))
    rider = models.ForeignKey(
        Rider, on_delete=models.CASCADE, related_name='combos')
    horse = models.ForeignKey(
        Horse, on_delete=models.CASCADE, verbose_name="Horse", related_name='combos')
    classes = models.ManyToManyField(
        Class, blank=True, through='ClassParticipation', related_name="combos")
    contact = models.CharField(
        max_length=100, choices=contact_choices, default="rider")
    email = models.EmailField(blank=True, null=True,
                              verbose_name="Contact Email")
    cell = models.CharField(max_length=12, blank=True,
                            verbose_name="Contact Cell Phone Number")
    show = models.ForeignKey(
        Show, on_delete=models.CASCADE, null=True, related_name='combos')

    def __str__(self):
        return f"Number: {self.num}, Rider: {self.rider.last_name}, Horse: {self.horse.name}, Show: {str(self.show.date)}"


def validate_unique(self, exclude=None):
    qs = HorseRiderCombo.objects.filter(rider=self.rider, horse=self.horse)
    if self.pk is None:
        if qs.filter(r=self.rider).exists() and qs.filter(h=self.horse.exists()):
            raise ValidationError("HRC already exists")


class ClassParticipation(models.Model):
    """
    Model for a ClassParticipation. Includes a participating class and a score for that class to be placed under a HorseRider Combo
    """
    class Meta:
        unique_together = ('participated_class', 'combo')
    participated_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="participations")

    combo = models.ForeignKey(HorseRiderCombo, verbose_name="Horse Rider Combination",
                              on_delete=models.CASCADE, related_name="participations")

    score = models.IntegerField(default=0)
    is_preregistered = models.BooleanField(default=False)

    def __str__(self):
        return f"Combo #{self.combo.num} participates in class {self.participated_class.num}"
