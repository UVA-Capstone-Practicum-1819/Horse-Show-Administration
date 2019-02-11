from django.test import TestCase, Client
import datetime
from show.models import *
from show.forms import *
from show.views import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from show import models
from django.urls import reverse
from django.http import HttpRequest
from .populatepdf import write_fillable_pdf, read_pdf, read_written_pdf


class CheckAge(TestCase):
    def test_calculate_age(self):
        rider = Rider.objects.create(name="Anna Wu", address="address1", city="cville", state="VA",
                                     zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        age = calculate_age(rider.birth_date)
        self.assertTrue(age == 15)

    def test_calculate_age2(self):
        rider1 = Rider.objects.create(name="Ashley Ontiri", address="address2", city="princeton", state="NJ", zip_code="2290310",
                                      email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('2010113', "%Y%m%d").date())
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        age = calculate_age(combo1.rider.birth_date)
        if age <= 14:
            self.assertTrue(combo1.rider.name == "Ashley Ontiri")


class CheckHorseType(TestCase):
    def test_horse_type_check(self):
        list = []
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(name="Anna Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        rider2 = Rider.objects.create(name="Ashley Ontiri", address="address2", city="princeton", state="NJ", zip_code="08541",
                                      email="ao@email.com", adult=True)
        rider3 = Rider.objects.create(name="Anne Katherine", address="address3", city="vienna", state="VA", zip_code="22181",
                                      email="ak@email.com", adult=False, birth_date=datetime.datetime.strptime('2010113', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=100, rider=rider2, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=100, rider=rider3, horse=horse3)
        if combo1.horse.type == "pony":
            list.append(combo1.rider.name)
        if combo2.horse.type == "pony":
            list.append(combo2.rider.name)
        if combo3.horse.type == "pony":
            list.append(combo3.rider.name)
        self.assertTrue("Ashley Ontiri" in list)
        self.assertFalse("Anna Wu" in list)


class CheckAdult(TestCase):
    def test_rider_is_adult(self):
        list = []
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(name="Anna Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        rider2 = Rider.objects.create(name="Ashley Ontiri", address="address2", city="princeton", state="NJ", zip_code="08541",
                                      email="ao@email.com", adult=True)
        rider3 = Rider.objects.create(name="Anne Katherine", address="address3", city="vienna", state="VA", zip_code="22181",
                                      email="ak@email.com", adult=False, birth_date=datetime.datetime.strptime('2010113', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=100, rider=rider2, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=100, rider=rider3, horse=horse3)
        if combo1.rider.adult is True:
            list.append(combo1.rider.name)
        if combo2.rider.adult is True:
            list.append(combo2.rider.name)
        if combo3.rider.adult is True:
            list.append(combo3.rider.name)
        self.assertTrue("Ashley Ontiri" in list)
        self.assertFalse("Anne Katherine" in list)


class CheckPonySize(TestCase):
    def test_pony_size_check(self):
        list = []
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(name="Anna Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        rider2 = Rider.objects.create(name="Ashley Ontiri", address="address2", city="princeton", state="NJ", zip_code="08541",
                                      email="ao@email.com", adult=True)
        rider3 = Rider.objects.create(name="Anne Katherine", address="address3", city="vienna", state="VA", zip_code="22181",
                                      email="ak@email.com", adult=False, birth_date=datetime.datetime.strptime('2010113', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=100, rider=rider2, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=100, rider=rider3, horse=horse3)
        if combo1.horse.size == "NA":
            self.assertTrue(combo1.horse.type == "horse")
        if combo2.horse.size == "large":
            list.append(combo2.rider.name)
        if combo3.horse.size == "large":
            list.append(combo3.rider.name)
        self.assertTrue(not list)
