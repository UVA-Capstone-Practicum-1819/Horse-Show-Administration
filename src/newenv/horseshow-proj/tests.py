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

# class ReadPdf(TestCase):
#     def test_read_pdf(self):
#         key = read_pdf("show/static/VHSA_Results_2015.pdf", 2, 1)
#         self.assertEqual(key, "p2_show_date")
#     def test_read_pdf2(self):
#         key = read_pdf("show/static/VHSA_Results_2015.pdf", 4, 2)
#         self.assertEqual(key, "p4_c1")
#
# class WritePdf(TestCase):
#     def test_write_pdf(self):
#         Show.objects.create(name="Show1", date="2019-10-07", location="Pony Barn")
#         show = Show.objects.get(date="2019-10-07")
#         d = {
#             'p2_show_name': show.name,
#             'p2_show_date': show.date,
#             }
#         write_fillable_pdf("show/static/VHSA_Results_2015.pdf",
#                        "show/static/VHSA_Final_Results.pdf", d)
#         value = read_written_pdf("show/static/VHSA_Final_Results.pdf", d, 2, 1)
#         self.assertEqual(value, show.date)
