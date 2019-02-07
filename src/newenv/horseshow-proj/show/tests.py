from django.test import TestCase, Client
from show.models import *
from show.forms import *
from show.views import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from show import models
from django.urls import reverse
from django.http import HttpRequest
from .populatepdf import write_fillable_pdf, read_pdf, read_written_pdf