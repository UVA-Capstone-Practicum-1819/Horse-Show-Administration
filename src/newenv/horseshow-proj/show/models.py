from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
import random

import datetime


class Classes(models.Model):
    number = models.IntegerField(default=0)
    first = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    third = models.IntegerField(default=0)
    fourth = models.IntegerField(default=0)
    fifth = models.IntegerField(default=0)
    sixth = models.IntegerField(default=0)

    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.number) + ". " + self.name


class Division(models.Model):
    name = models.CharField(max_length=100, default="")
    number = models.IntegerField(default=0)

    champion = models.IntegerField(default=0)
    champion_pts = models.IntegerField(default=0)
    champion_reserve = models.IntegerField(default=0)
    champion_reserve_pts = models.IntegerField(default=0)

    classes = models.ManyToManyField(Classes)

    def __str__(self):
        return self.name


class Show(models.Model):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100, primary_key=True)
    location = models.CharField(max_length=100)
    dayOfPrice = models.IntegerField(null=True, blank=True)
    preRegistrationPrice = models.IntegerField(null=True, blank=True)

    divisions = models.ManyToManyField(Division, blank=True)

    def __str__(self):
        return self.date


class Horse(models.Model):

    size_choices = (
        ("NA", "N/A"),
        ("small", "SM"),
        ("medium", "MED"),
        ("large", "LG"),
    )

    type_choices = (
        ("horse", "Horse"),
        ("pony", "Pony"),
    )

    name = models.CharField(
        primary_key=True, max_length=200, verbose_name="Name (Barn Name)")

    accession_no = models.IntegerField(verbose_name="Accession Number")

    coggins_date = models.DateField(
        default=datetime.date.today,  verbose_name="Coggins Date", )

    owner = models.CharField(max_length=200, verbose_name="Owner")

    type = models.CharField(
        max_length=200, choices=type_choices, default="Horse", verbose_name="Type")

    size = models.CharField(
        max_length=200, choices=size_choices, default="N/A", verbose_name="Size")

    def __str__(self):
        return self.name


class Rider (models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")

    address = models.CharField(max_length=200, verbose_name="Address")

    email = models.EmailField(
        primary_key=True, max_length=200, validators=[EmailValidator()], verbose_name="Email")

    birth_date = models.DateField(
        blank=True, null=True, verbose_name="Birth Date", )

    member_VHSA = models.BooleanField(
        default=False, blank=True, verbose_name="Member of the VHSA")

    county = models.CharField(
        max_length=200, blank=True, verbose_name="If member of 4H, specify county")

    horses = models.ManyToManyField(Horse, through='HorseRiderCombo')

    def __str__(self):
        return self.name


class ClassScore(models.Model):
    participated_class = models.ForeignKey(Classes, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return str(self.score)


class HorseRiderCombo(models.Model):
    contact_choices = (
        ("rider", "Rider"),
        ("owner", "Owner"),
        ("parent", "Parent"),
        ("trainer", "Trainer")
    )
    num = models.IntegerField(primary_key=True, validators=[
        MinValueValidator(100), MaxValueValidator(999)], verbose_name="Combination Number")

    rider = models.ForeignKey(
        Rider, on_delete=models.CASCADE, verbose_name="Rider")

    horse = models.ForeignKey(
        Horse, on_delete=models.CASCADE, verbose_name="Horse")

    classes = models.ManyToManyField(Classes, verbose_name="Classes")

    class_scores = models.ManyToManyField(
        ClassScore, verbose_name="Class Scores", blank=True, null=True)


    contact = models.CharField(max_length=100,
                               choices=contact_choices, default="rider", verbose_name="Contact")


    email = models.EmailField(blank=True,
                              null=True, verbose_name="Contact Email")

    cell = models.CharField(max_length=12,
                            blank=True, verbose_name="Contact Cell Phone Number")

    def __str__(self):
        return str(self.num)
