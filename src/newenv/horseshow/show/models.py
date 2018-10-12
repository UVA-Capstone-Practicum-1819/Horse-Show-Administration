from django.db import models

# Create your models here.
class Show(models.Model):
    show_name = models.charField(max_length=100)
    show_date = models.charField(max_length=100)
    show_location = models.charField(max_length=100)
    def __str__(self):
        return self.show_name
