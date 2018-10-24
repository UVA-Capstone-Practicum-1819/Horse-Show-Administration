from django.test import TestCase
from show.models import Show, Rider, Horse

# Create your tests here.


class ShowTestCase(TestCase):
    def setUp(self):
        Show.objects.create(show_name = "boo palooza", show_date = "10/09/2018", show_location = "Berry Farm")
        Show.objects.create(show_name = "Horse Show Level 1", show_date = "10/03/2015", show_location = "Pony Day Farm")
