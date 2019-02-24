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

    def test_select_combo(self):
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get(reverse('select_combo', kwargs={'show_date':'2018-12-10'}))

    def test_select_show_post(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.post('/show/', {'date':'2018-12-10'})

    def test_select_combo_billing_post(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        rider1 = Rider.objects.create(name="Anna Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=200, rider=rider1, horse=horse1, show=show)
        c1 = Class.objects.create(name="Test", num="1")
        c2 = Class.objects.create(name="Test2", num="2")
        class_participation = ClassParticipation.objects.create(participated_class=c1, combo=combo1, is_preregistered=False)
        class_participation = ClassParticipation.objects.create(participated_class=c2, combo=combo1, is_preregistered=True)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/combo/select', {'combo':combo1.pk})
        self.assertRedirects(response, '/show/2018-12-10/combo/200/billing')

class AttemptedTestCases(TestCase):
    def test_rank_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/1/rank', {'first':100, 'second':200, 'third':300, 'fourth':400, 'fifth':500, 'sixth':600})

    def test_incorrect_rank_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/1/rank', {'first':1, 'second':2, 'third':3, 'fourth':40, 'fifth':50, 'sixth':60})

    def test_empty_rank_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/1/rank', {'first':'', 'second':'', 'third':'', 'fourth':'', 'fifth':'', 'sixth':''})

    def test_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get('/show/2018-12-10/division/1/class/1/rank')

    def test_add_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
<<<<<<< HEAD
        response = self.client.post('/show/2018-12-10/division/1/class/1/rank', {'first':100, 'second':200, 'third':300, 'fourth':400, 'fifth':500, 'sixth':600})
=======
        response = self.client.post('/show/2018-12-10/combo/select', {'combo':'200'})


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


class CheckEntryNum(TestCase):
    def test_entry_num(self):
        list = []
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(name="Anna Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())

        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse3)

        show = Show.objects.create(date=datetime.datetime.strptime('20190526', "%Y%m%d"), name="Show1",
        location="Cville", day_of_price=15, pre_reg_price=11)
        div = Division.objects.create(id=1, name="Div1",show = show)
        c1 = Class.objects.create(num=1, name="Class1", division=div, show = show)
        part1 = ClassParticipation.objects.create(participated_class=c1, combo=combo1)
        part2 = ClassParticipation.objects.create(participated_class=c1, combo=combo2)
        part3 = ClassParticipation.objects.create(participated_class=c1, combo=combo3)
        num_entry = ClassParticipation.objects.filter(participated_class=c1).count()
        self.assertTrue(num_entry == 3)

class CheckRankClassForm(TestCase):
    def test_rank_form(self):
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(name="Anna Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())

        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=101, rider=rider1, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=102, rider=rider1, horse=horse3)

        form_data = {'first': combo1.num, 'second':combo2.num, 'third':combo3.num}
        form = RankingForm(data=form_data)
        self.assertTrue(form.is_valid())

class CheckRankDatabaseValidation(TestCase):
    def test_rank_database_validation(self):
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(name="Anna Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())

        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=101, rider=rider1, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=102, rider=rider1, horse=horse3)

        show = Show.objects.create(date=datetime.datetime.strptime('20190526', "%Y%m%d"), name="Show1",
        location="Cville", day_of_price=15, pre_reg_price=11)
        div = Division.objects.create(id=1, name="Div1",show = show)
        c1 = Class.objects.create(num=1, name="Class1", division=div, show = show)

        form_data = {'first': 100, 'second':110, 'third':120}
        form = RankingForm(data=form_data)
        if form.is_valid():
            rank_list = [form.cleaned_data['first'], form.cleaned_data['second'], form.cleaned_data['third'],form.cleaned_data['fourth'],form.cleaned_data['fifth'],form.cleaned_data['sixth']]
        try:
            if HorseRiderCombo.objects.get(num=rank_list[1]):
                c1.second = rank_list[1]
        except:
            print("")
        try:
            if HorseRiderCombo.objects.get(num=rank_list[0]):
                c1.first = rank_list[0]
        except:
            print("")
        self.assertFalse(c1.second==110)
        self.assertTrue(c1.first==100)

class CheckRankRangeValidation(TestCase):
    def test_rank_range_validation(self):
        show = Show.objects.create(date=datetime.datetime.strptime('20190526', "%Y%m%d"), name="Show1",
        location="Cville", day_of_price=15, pre_reg_price=11)
        div = Division.objects.create(id=1, name="Div1",show = show)
        c1 = Class.objects.create(num=1, name="Class1", division=div, show = show)

        form_data = {'first': 1, 'second':9990, 'third':120}
        form = RankingForm(data=form_data)
        if form.is_valid():
            rank_list = [form.cleaned_data['first'], form.cleaned_data['second'], form.cleaned_data['third'],form.cleaned_data['fourth'],form.cleaned_data['fifth'],form.cleaned_data['sixth']]
        try:
            if 100<=rank_list[1]<=999:
                c1.second = rank_list[1]
        except:
            print("")
        try:
            if 100<=rank_list[1]<=999:
                c1.first = rank_list[0]
        except:
            print("")
        self.assertFalse(c1.second==9990)
        self.assertFalse(c1.first==1)

class CheckRankRepeatValidation(TestCase):
    def test_rank_repeat_validation(self):
        show = Show.objects.create(date=datetime.datetime.strptime('20190526', "%Y%m%d"), name="Show1",
        location="Cville", day_of_price=15, pre_reg_price=11)
        div = Division.objects.create(id=1, name="Div1",show = show)
        c1 = Class.objects.create(num=1, name="Class1", division=div, show = show)

        form_data = {'first': 100, 'second':100, 'third':110}
        form = RankingForm(data=form_data)
        if form.is_valid():
            rank_list = [form.cleaned_data['first'], form.cleaned_data['second'], form.cleaned_data['third'],form.cleaned_data['fourth'],form.cleaned_data['fifth'],form.cleaned_data['sixth']]
        rank_list_without_none = [x for x in rank_list if x is not None]
        if len(set(rank_list_without_none)) != len(rank_list_without_none):
            str = "Same combination entered for more than one rank. Duplicates are not allowed in ranking."
        else:
            c1.first = rank_list[0]
            c1.second = rank_list[1]
            c1.third = rank_list[2]
        self.assertTrue(c1.second is None)
        self.assertEqual(str,"Same combination entered for more than one rank. Duplicates are not allowed in ranking.")
