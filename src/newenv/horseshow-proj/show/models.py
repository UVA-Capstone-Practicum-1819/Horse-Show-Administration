from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
import random


class Classes(models.Model):
    class_name = models.CharField(max_length=100, default="")
    class_number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.class_number) + ". " + self.class_name


class Division(models.Model):
    division_name = models.CharField(max_length=100, default="")
    division_number = models.IntegerField(default=0)
    classes = models.ManyToManyField(Classes, blank=True, null=True)

    def __str__(self):
        return self.division_name


class Show(models.Model):
    show_name = models.CharField(max_length=100)
    show_date = models.DateField(primary_key=True)
    show_location = models.CharField(max_length=100)
    show_divisions = models.ManyToManyField(Division, blank=True, null=True)
    dayOfPrice = models.IntegerField(null=True, blank=True)
    preRegistrationPrice = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.show_name


class Horse (models.Model):
    name = models.CharField(max_length=200)
    barn_name = models.CharField(max_length=200)
    age = models.IntegerField()
    coggins = models.IntegerField()
    owner = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Rider (models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)])
    email = models.EmailField(max_length=200, validators=[EmailValidator()])
    horses = models.ManyToManyField(Horse, through='HorseRiderCombo')

    def __str__(self):
        return self.name


class HorseRiderCombo(models.Model):
    num = models.IntegerField(primary_key=True, default=-1)
    rider = models.ForeignKey(
        Rider, on_delete=models.CASCADE)
    horse = models.ForeignKey(
        Horse, on_delete=models.CASCADE)
