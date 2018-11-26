from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
import random


class Classes(models.Model):
    name = models.CharField(max_length=100, default="")
    number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.number) + ". " + self.name


class Division(models.Model):
    name = models.CharField(max_length=100, default="")
    number = models.IntegerField(default=0)
    classes = models.ManyToManyField(Classes)

    def __str__(self):
        return self.name


class Show(models.Model):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100, primary_key=True)
    location = models.CharField(max_length=100)
    divisions = models.ManyToManyField(Division, blank=True)
    dayOfPrice = models.IntegerField(null=True, blank=True)
    preRegistrationPrice = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.date


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
    email = models.EmailField(
        primary_key=True, max_length=200, validators=[EmailValidator()])
    horses = models.ManyToManyField(Horse, through='HorseRiderCombo')

    def __str__(self):
        return self.name


class HorseRiderCombo(models.Model):
    num = models.IntegerField()
    rider = models.ForeignKey(
        Rider, on_delete=models.CASCADE)
    horse = models.ForeignKey(
        Horse, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.num)
