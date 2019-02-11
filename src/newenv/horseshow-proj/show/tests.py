from django.test import TestCase, Client
from show.models import *
from show.forms import *
from show.views import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from show import models
from django.urls import reverse
from django.http import HttpRequest

class BillTests(TestCase):
    def test_billpage_setup(self):
        horse1 = Horse.objects.create(name="Lollipop", coggins_date="2011-10-11", accession_num=48, owner="John", size="medium", type="horse")
        rider1 = Rider.objects.create(name = "Bob", address="555 ct", birth_date="1990-09-25", email="55@s.edu", member_VHSA=True, county="fairfax")
        c1 = Class.objects.create(name="Test", num="1")
        combo = HorseRiderCombo.objects.create(num = 555, rider = rider1, horse = horse1)
        class_participation = ClassParticipation(participated_class=c1, combo=combo, is_preregistered=False)
        self.assertFalse(class_participation.is_preregistered)

    def test_billpage_pricecheck(self):
        horse1 = Horse.objects.create(name="Lollipop", coggins_date="2011-10-11", accession_num=48, owner="John", size="medium", type="horse")
        rider1 = Rider.objects.create(name = "Bob", address="555 ct", birth_date="1990-09-25", email="55@s.edu", member_VHSA=True, county="fairfax")
        c2 = Class.objects.create(name="Test2", num="2")
        combo = HorseRiderCombo.objects.create(num = 555, rider = rider1, horse = horse1)
        class_participation = ClassParticipation(participated_class=c2, combo=combo, is_preregistered=True)
        self.assertTrue(class_participation.is_preregistered)

class Add_Combo_Classes(TestCase):
    def add_classes_to_combo(self):
        horse1 = Horse.objects.create(name="Lollipop", coggins_date="2011-10-11", accession_num=48, owner="John", size="medium", type="horse")
        rider1 = Rider.objects.create(name = "Bob", address="555 ct", birth_date="1990-09-25", email="55@s.edu", member_VHSA=True, county="fairfax")
        c1 = Class.objects.create(name="Test", num="1")
        combo = HorseRiderCombo.objects.create(num = 555, rider = rider1, horse = horse1)
        class_participation = ClassParticipation(participated_class=c1, combo=combo, is_preregistered=False)
        self.assertEqual(c1, class_participation.participated_class)

    def wrong_class_for_combo(self):
        horse1 = Horse.objects.create(name="Lollipop", coggins_date="2011-10-11", accession_num=48, owner="John", size="medium", type="horse")
        rider1 = Rider.objects.create(name = "Bob", address="555 ct", birth_date="1990-09-25", email="55@s.edu", member_VHSA=True, county="fairfax")
        c1 = Class.objects.create(name="Test", num="1")
        combo = HorseRiderCombo.objects.create(num = 555, rider = rider1, horse = horse1)
        class_participation = ClassParticipation(participated_class=c1, combo=combo, is_preregistered=False)
        self.assertFalse(combo, class_participation.combo)

    def classparticipation_form_invalid(self):
        class_participation = ClassParticipation(participated_class=c1, combo=combo, is_preregistered=True)
        self.assertTrue(isinstance(class_participation, ClassParticipation))
