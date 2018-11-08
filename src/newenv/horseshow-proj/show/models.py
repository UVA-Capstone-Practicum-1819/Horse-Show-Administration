from django.db import models
import random

class Classes(models.Model):
    class_name = models.CharField(max_length=100, default = "")
    class_number = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.class_number) + ". " + self.class_name

class Show(models.Model):
    show_name = models.CharField(max_length=100)
    show_date = models.CharField(max_length=100)
    show_location = models.CharField(max_length=100)

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
    age = models.IntegerField()
    email = models.CharField(max_length=200)
    horses = models.ManyToManyField(Horse, through='HorseRiderCombo')

    def __str__(self):
        return self.name

class HorseRiderCombo(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    num = models.IntegerField()

def random_string():
    rand_str = ""
    for i in range(3):
        rand_str += random.choice("0123456789")
    return rand_str
    # return str(random.randint(100, 999))
