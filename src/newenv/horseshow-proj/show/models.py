from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
import random

import datetime


class Show(models.Model):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100, primary_key=True)
    location = models.CharField(max_length=100)
    dayOfPrice = models.IntegerField(null=True, blank=True)
    preRegistrationPrice = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.date


class Division(models.Model):
    name = models.CharField(max_length=100, default="")
    number = models.IntegerField(default=0)

    champion = models.IntegerField(default=0)
    champion_pts = models.IntegerField(default=0)
    champion_reserve = models.IntegerField(default=0)
    champion_reserve_pts = models.IntegerField(default=0)

    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Classes(models.Model):
    number = models.IntegerField(default=0)
    first = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    third = models.IntegerField(default=0)
    fourth = models.IntegerField(default=0)
    fifth = models.IntegerField(default=0)
    sixth = models.IntegerField(default=0)

    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return division.name + " " + str(self.number)


class Horse (models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    accession_no = models.IntegerField()
    coggins_date = models.DateField(default=datetime.date.today)
    owner = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Rider (models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField(
        primary_key=True, max_length=200, validators=[EmailValidator()])
    birth_date = models.DateField(blank=True, null=True)
    member_VHSA = models.BooleanField(default=False)
    county = models.CharField(max_length=200, blank=True)
    horses = models.ManyToManyField(Horse, through='HorseRiderCombo')

    def __str__(self):
        return self.name


class ClassScore(models.Model):
    participated_class = models.ForeignKey(Classes, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return str(self.score)


class HorseRiderCombo(models.Model):
    num = models.IntegerField(primary_key=True, validators=[
        MinValueValidator(0), MaxValueValidator(999)])
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    classes = models.ManyToManyField(Classes)
    class_scores = models.ManyToManyField(ClassScore)
    contact = models.CharField(max_length=2,
                               choices=(("RIDER", "Rider"), ("OWNER", "Owner"), ("PARENT", "Parent"), ("TRAINER", "Trainer")), default="RIDER")
    email = models.EmailField(unique=True, blank=True, null=True)
    cell = models.CharField(max_length=200, unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.num)
