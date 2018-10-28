from django.db import models

# Create your models here.

class Show(models.Model):
    show_name = models.CharField(max_length=100)
    show_date = models.CharField(max_length=100)
    show_location = models.CharField(max_length=100)
    def __str__(self):
        return self.show_name

class Rider (models.Model):
    name= models.CharField(max_length= 200)
    address = models.CharField(max_length=200)
    age= models.IntegerField()
    email = models.CharField(max_length=200)

class Horse (models.Model):
    name= models.CharField(max_length= 200)
    barn_name = models.CharField(max_length=200)
    age= models.IntegerField()
    coggins= models.IntegerField()
    owner = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    def __str__(self):
        return self.name
