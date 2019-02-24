from django.test import TestCase, Client
import datetime
from show.models import *
from show.forms import *
from show.views import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from show import models
from unittest.mock import Mock
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

class ViewsTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_add_show_get(self):
           show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
           new_division = Division.objects.create(name="division")
           request = HttpRequest()
           client = Client()
           response = client.get(reverse('add_show'))

    def test_add_show_post(self):
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/add', {'name':'test', 'date':'2018-12-10', 'location':'here', 'day_of_price':10, 'pre_reg_price':5})
        self.assertRedirects(response, '/show/2018-12-10/')

    def test_view_show(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.get(reverse('view_show', kwargs={'show_date':'2018-12-10'}))

    def test_view_show(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/', {'num':200})
        response.content

    def test_select_show(self):
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get(reverse('select_show'))

    def test_select_show_post(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.post('/show/', {'date':'2018-12-10'})

    def sign_up_test(self):
        request = HttpRequest()
        client = Client()
        response = client.get('/show/signup/')
