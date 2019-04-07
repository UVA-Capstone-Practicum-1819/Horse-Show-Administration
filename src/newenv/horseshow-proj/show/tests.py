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
from .labels import generate_show_labels
from django.db import IntegrityError
from contextlib import contextmanager


class BillTests(TestCase):
    def test_billpage_setup(self):
        horse1 = Horse.objects.create(name="Lollipop", coggins_date="2011-10-11",
                                      accession_num=48, owner="John", size="medium", type="horse")
        rider1 = Rider.objects.create(first_name="Bob",last_name="Test", address="555 ct", birth_date="1990-09-25",
                                      email="55@s.edu", member_VHSA=True, county="fairfax")
        c1 = Class.objects.create(name="Test", num="1")
        combo = HorseRiderCombo.objects.create(
            num=555, rider=rider1, horse=horse1)
        class_participation = ClassParticipation(
            participated_class=c1, combo=combo)
        #self.assertFalse(class_participation.is_preregistered)

    def test_billpage_pricecheck(self):
        horse1 = Horse.objects.create(name="Lollipop", coggins_date="2011-10-11",
                                      accession_num=48, owner="John", size="medium", type="horse")
        rider1 = Rider.objects.create(first_name="Bob", last_name="Test", address="555 ct", birth_date="1990-09-25",
                                      email="55@s.edu", member_VHSA=True, county="fairfax")
        c2 = Class.objects.create(name="Test2", num="2")
        combo = HorseRiderCombo.objects.create(
            num=555, rider=rider1, horse=horse1)
        class_participation = ClassParticipation(
            participated_class=c2, combo=combo)
        # self.assertTrue(class_participation.is_preregistered)


class Add_Combo_Classes(TestCase):
    def add_classes_to_combo(self):
        horse1 = Horse.objects.create(name="Lollipop", coggins_date="2011-10-11",
                                      accession_num=48, owner="John", size="medium", type="horse")
        rider1 = Rider.objects.create(name="Bob", address="555 ct", birth_date="1990-09-25",
                                      email="55@s.edu", member_VHSA=True, county="fairfax")
        c1 = Class.objects.create(name="Test", num="1")
        combo = HorseRiderCombo.objects.create(
            num=555, rider=rider1, horse=horse1)
        class_participation = ClassParticipation(
            participated_class=c1, combo=combo)
        self.assertEqual(c1, class_participation.participated_class)

    def wrong_class_for_combo(self):
        horse1 = Horse.objects.create(name="Lollipop", coggins_date="2011-10-11",
                                      accession_num=48, owner="John", size="medium", type="horse")
        rider1 = Rider.objects.create(name="Bob", address="555 ct", birth_date="1990-09-25",
                                      email="55@s.edu", member_VHSA=True, county="fairfax")
        c1 = Class.objects.create(name="Test", num="1")
        combo = HorseRiderCombo.objects.create(
            num=555, rider=rider1, horse=horse1)
        class_participation = ClassParticipation(
            participated_class=c1, combo=combo)
        self.assertFalse(combo, class_participation.combo)

    def classparticipation_form_invalid(self):
        class_participation = ClassParticipation(
            participated_class=c1, combo=combo)
        self.assertTrue(isinstance(class_participation, ClassParticipation))


class CheckAge(TestCase):
    def test_calculate_age(self):
        rider = Rider.objects.create(first_name="Anna", last_name="Wu", address="address1", city="cville", state="VA",
                                     zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        age = calculate_age(rider.birth_date)
        self.assertTrue(age == 15)

    def test_calculate_age2(self):
        rider1 = Rider.objects.create(first_name="Ashley", last_name="Ontiri", city="princeton", state="NJ", zip_code="2290310",
                                      email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('2010113', "%Y%m%d").date())
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        age = calculate_age(combo1.rider.birth_date)
        if age <= 14:
            self.assertTrue(combo1.rider.first_name == "Ashley")


# class TestPdf(TestCase):
#     def test_pdf(self):
#         show = Show.objects.create(
#             name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
#         new_division = Division.objects.create(name="division")
#         request = HttpRequest()
#         p = populate_pdf(request, '2018-12-10')
#         url = reverse("populate_pdf", kwargs={'show_date': '2018-12-10'})
#         resp = self.client.get(url)

#         self.assertEqual(resp.status_code, 302)


class CheckHorseType(TestCase):
    def test_horse_type_check(self):
        list = []
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(first_name="Anna", last_name="Wu", address="address1", city="cville", state="VA",
            zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        rider2 = Rider.objects.create(first_name="Ashley", last_name="Ontiri", address="address2", city="princeton", state="NJ",
            zip_code="08541", email="ao@email.com", adult=True)
        rider3 = Rider.objects.create(first_name="Anne",last_name="Katherine", address="address3", city="vienna", state="VA", zip_code="22181",
            email="ak@email.com", adult=False, birth_date=datetime.datetime.strptime('2010113', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=100, rider=rider2, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=100, rider=rider3, horse=horse3)
        if combo1.horse.type == "pony":
            list.append(combo1.rider.first_name)
        if combo2.horse.type == "pony":
            list.append(combo2.rider.first_name)
        if combo3.horse.type == "pony":
            list.append(combo3.rider.first_name)
        self.assertTrue("Ashley" in list)
        self.assertFalse("Anna" in list)


class CheckAdult(TestCase):
    def test_rider_is_adult(self):
        list = []
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(first_name="Anna", last_name="Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        rider2 = Rider.objects.create(first_name="Ashley", last_name="Ontiri", address="address2", city="princeton", state="NJ", zip_code="08541",
                                      email="ao@email.com", adult=True)
        rider3 = Rider.objects.create(first_name="Anne",last_name="Katherine", address="address3", city="vienna", state="VA", zip_code="22181",
                                      email="ak@email.com", adult=False, birth_date=datetime.datetime.strptime('2010113', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=100, rider=rider2, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=100, rider=rider3, horse=horse3)
        if combo1.rider.adult is True:
            list.append(combo1.rider.first_name)
        if combo2.rider.adult is True:
            list.append(combo2.rider.first_name)
        if combo3.rider.adult is True:
            list.append(combo3.riderfirst_name)
        self.assertTrue("Ashley" in list)
        self.assertFalse("Anne" in list)


class CheckPonySize(TestCase):
    def test_pony_size_check(self):
        list = []
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(first_name="Anna", last_name="Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        rider2 = Rider.objects.create(first_name="Ashley", last_name="Ontiri", address="address2", city="princeton", state="NJ", zip_code="08541",
                                      email="ao@email.com", adult=True)
        rider3 = Rider.objects.create(first_name="Anne",last_name="Katherine", address="address3", city="vienna", state="VA", zip_code="22181",
                                      email="ak@email.com", adult=False, birth_date=datetime.datetime.strptime('2010113', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=100, rider=rider2, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=100, rider=rider3, horse=horse3)
        if combo1.horse.size == "N/A":
            self.assertTrue(combo1.horse.type == "horse")
        if combo2.horse.size == "large":
            list.append(combo2.rider.first_name)
        if combo3.horse.size == "large":
            list.append(combo3.rider.first_name)
        self.assertTrue(not list)



class ViewsTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')

    def test_add_show_get(self):
        show = Show.objects.create(
            name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        new_division = Division.objects.create(name="division")
        request = HttpRequest()
        client = Client()
        response = client.get(reverse('add_show'))

    def test_add_show_post(self):
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post(
            '/show/add', {'name': 'test', 'date': '2018-12-10', 'location': 'here', 'day_of_price': 10, 'pre_reg_price': 5})
        self.assertRedirects(response, '/show/2018-12-10/view')

    def test_view_show(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(
            name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.get(
            reverse('view_show', kwargs={'show_date': '2018-12-10'}))

    def test_view_show(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(
            name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        rider1 = Rider.objects.create(first_name="Anna", last_name ="Wu", address="address1", city="cville", state="VA",zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=200, rider=rider1, horse=horse1, show = show)
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/', {'num': 200})
        response.content

    def test_view_show_post_dne(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(
            name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        rider1 = Rider.objects.create(first_name="Anna", last_name ="Wu", address="address1", city="cville", state="VA",zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=200, rider=rider1, horse=horse1, show = show)
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/', {'num': 201})
        response.content

    def test_select_show(self):
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get(reverse('select_show'))

    def test_select_show_post(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(
            name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.post('/show/', {'date': '2018-12-10'})



class CheckAdult(TestCase):
    def test_rider_is_adult(self):
        list = []
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(first_name="Anna",last_name="Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        rider2 = Rider.objects.create(first_name="Ashley", last_name= "Ontiri", address="address2", city="princeton", state="NJ", zip_code="08541",
                                      email="ao@email.com", adult=True)
        rider3 = Rider.objects.create(first_name="Anne", last_name="Katherine", address="address3", city="vienna", state="VA", zip_code="22181",
                                      email="ak@email.com", adult=False, birth_date=datetime.datetime.strptime('2010113', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=100, rider=rider2, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=100, rider=rider3, horse=horse3)
        if combo1.rider.adult is True:
            list.append(combo1.rider.first_name)
        if combo2.rider.adult is True:
            list.append(combo2.rider.first_name)
        if combo3.rider.adult is True:
            list.append(combo3.rider.first_name)
        self.assertTrue("Ashley" in list)
        self.assertFalse("Anne" in list)


class CheckEntryNum(TestCase):
    def test_entry_num(self):
        list = []
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(first_name="Anna", last_name="Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())

        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse3)

        show = Show.objects.create(date=datetime.datetime.strptime('20190526', "%Y%m%d"), name="Show1",
                                   location="Cville", day_of_price=15, pre_reg_price=11)
        div = Division.objects.create(id=1, name="Div1", show=show)
        c1 = Class.objects.create(
            num=1, name="Class1", division=div, show=show)
        part1 = ClassParticipation.objects.create(
            participated_class=c1, combo=combo1)
        part2 = ClassParticipation.objects.create(
            participated_class=c1, combo=combo2)
        part3 = ClassParticipation.objects.create(
            participated_class=c1, combo=combo3)
        num_entry = ClassParticipation.objects.filter(
            participated_class=c1).count()
        self.assertTrue(num_entry == 3)

    def test_add_existing_class_num(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(
            name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        div = Division.objects.create(id=1, name="Div1", show=show)
        c1 = Class.objects.create(num=1, name="Class1", division=div, show=show)

        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        rider1 = Rider.objects.create(first_name="Anna", last_name ="Wu", address="address1", city="cville", state="VA",zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=200, rider=rider1, horse=horse1, show = show)
        part1 = ClassParticipation.objects.create(participated_class=c1, combo=combo1)
        form = ClassComboForm()
        if ClassParticipation.objects.filter(participated_class=c1) is None:
            form_data = {'is_preregistered': False,
                        'num': 1}
            form = ClassComboForm(data=form_data)
        self.assertFalse(form.is_valid())


class CheckRankClassForm(TestCase):
    def test_rank_form(self):
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        horse2 = Horse.objects.create(name="Watchme", coggins_date=datetime.datetime.strptime(
            '20090811', "%Y%m%d").date(), accession_num="ace321", owner="Angie Lee", type="pony", size="small")
        horse3 = Horse.objects.create(name="Strange", coggins_date=datetime.datetime.strptime(
            '20110524', "%Y%m%d").date(), accession_num="ace567", owner="Sarah Chu", type="pony", size="medium")
        rider1 = Rider.objects.create(first_name="Anna",last_name= "Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())

        combo1 = HorseRiderCombo.objects.create(
            num=100, rider=rider1, horse=horse1)
        combo2 = HorseRiderCombo.objects.create(
            num=101, rider=rider1, horse=horse2)
        combo3 = HorseRiderCombo.objects.create(
            num=102, rider=rider1, horse=horse3)
        show = Show.objects.create(date=datetime.datetime.strptime('20190526', "%Y%m%d"), name="Show1",
                                   location="Cville", day_of_price=15, pre_reg_price=11)
        div = Division.objects.create(id=1, name="Div1", show=show)
        c1 = Class.objects.create(
            num=1, name="Class1", division=div, show=show)

        form_data = {'first': 100, 'second': 110, 'third': 120}
        form = RankingForm(data=form_data)
        if form.is_valid():
            rank_list = [form.cleaned_data['first'], form.cleaned_data['second'], form.cleaned_data['third'],
                         form.cleaned_data['fourth'], form.cleaned_data['fifth'], form.cleaned_data['sixth']]

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

        self.assertFalse(c1.second == 110)
        self.assertTrue(c1.first == 100)


class CheckRankRangeValidation(TestCase):
    def test_rank_range_validation(self):
        show = Show.objects.create(date=datetime.datetime.strptime('20190526', "%Y%m%d"), name="Show1",
                                   location="Cville", day_of_price=15, pre_reg_price=11)
        div = Division.objects.create(id=1, name="Div1", show=show)
        c1 = Class.objects.create(
            num=1, name="Class1", division=div, show=show)

        form_data = {'first': 1, 'second': 9990, 'third': 120}
        form = RankingForm(data=form_data)
        if form.is_valid():
            rank_list = [form.cleaned_data['first'], form.cleaned_data['second'], form.cleaned_data['third'],
                         form.cleaned_data['fourth'], form.cleaned_data['fifth'], form.cleaned_data['sixth']]
        try:
            if 100 <= rank_list[1] <= 999:

                c1.second = rank_list[1]
        except:
            print("")
        try:

            if 100 <= rank_list[1] <= 999:

                c1.first = rank_list[0]
        except:
            print("")
        self.assertFalse(c1.second == 9990)
        self.assertFalse(c1.first == 1)


class CheckRankRepeatValidation(TestCase):
    def test_rank_repeat_validation(self):
        show = Show.objects.create(date=datetime.datetime.strptime('20190526', "%Y%m%d"), name="Show1",
                                   location="Cville", day_of_price=15, pre_reg_price=11)
        div = Division.objects.create(id=1, name="Div1", show=show)
        c1 = Class.objects.create(
            num=1, name="Class1", division=div, show=show)

        form_data = {'first': 100, 'second': 100, 'third': 110}
        form = RankingForm(data=form_data)
        if form.is_valid():
            rank_list = [form.cleaned_data['first'], form.cleaned_data['second'], form.cleaned_data['third'],
                         form.cleaned_data['fourth'], form.cleaned_data['fifth'], form.cleaned_data['sixth']]
        rank_list_without_none = [x for x in rank_list if x is not None]
        if len(set(rank_list_without_none)) != len(rank_list_without_none):
            str = "Same combination entered for more than one rank. Duplicates are not allowed in ranking."
        else:
            c1.first = rank_list[0]
            c1.second = rank_list[1]
            c1.third = rank_list[2]
        self.assertTrue(c1.second is None)
        self.assertEqual(
            str, "Same combination entered for more than one rank. Duplicates are not allowed in ranking.")


class CheckRider(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'some_user', 'lennon@thebeatles.com', 'johnpassword')
        self.user.save()
        self.client = Client()
        self.client.force_login(self.user)

        self.show = Show.objects.create(
            date='2019-10-12', pre_reg_price=5, day_of_price=2, name="5th annual", location="some_place")

        self.rider1 = Rider.objects.create(first_name="Bob",last_name="Test",address="555 ct", birth_date="1990-09-25",
                                           email="55@s.edu", member_VHSA=True, county="fairfax")

        self.rider2 = Rider.objects.create(first_name="Ashley",last_name="Ontiri", address="address2", city="princeton", zip_code="22903",
                                           email="ao@email.com", adult=True, birth_date="1996-10-15", member_VHSA=False, county="Loudoun")

        self.rider1.show = self.show
        self.rider2.show = self.show

    def test_view_riders_get(self):
        response = self.client.get(reverse('view_riders'))
    
    def test_delete_rider_get(self):
        response = self.client.get(
            reverse('delete_rider', kwargs={"rider_pk": self.rider1.pk}))


    def test_update_rider_add_post(self):
        
        response = self.client.post(
            reverse('add_rider'), data={'name': "some new name", 'address': "some new address", 'city': "some city", 'state': "VA", 'zip_code': 22903,
             'birth_date': self.rider2.birth_date, 'member_VHSA': False, 'county': "some county"})

    def test_update_rider_edit_post(self):
        
        response = self.client.post(
            reverse('edit_rider', kwargs={"rider_pk": self.rider1.pk}), data={'name': "some new name", 'address': "some new address", 'city': "some city", 'state': "VA", 'zip_code': 22903,
             'birth_date': self.rider2.birth_date, 'member_VHSA': False, 'county': "some county"})             

    def test_update_rider_valid(self):
        
        response = self.client.post(
            reverse('add_rider'), data={'first_name': "firstname", "last_name": "LastName", 'address': "some new address", 'city': "some city", 'state': "VA", 'zip_code': 22903, 'email': "someemail@virignia.edu",
             'birth_date': self.rider2.birth_date, 'member_VHSA': False, 'county': "some county"})

    def test_get_rider_form_add_get(self):
        response = self.client.get(reverse('get_rider_form'))
    
    def test_get_rider_form_edit_get(self):
        response = self.client.get(reverse('get_rider_form_edit', kwargs={"rider_pk": self.rider1.pk}))

    

class CheckHorse(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'some_user', 'lennon@thebeatles.com', 'johnpassword')
        self.user.save()
        self.client = Client()
        self.client.force_login(self.user)

        self.show = Show.objects.create(
            date='2019-10-12', pre_reg_price=5, day_of_price=2, name="5th annual", location="some_place")

        self.horse1 = Horse.objects.create(name="Lollipop", coggins_date="2011-10-11",
                                      accession_num=48, owner="John", size="medium", type="horse")
        self.horse2 = Horse.objects.create(name="Marshmallow", coggins_date="2012-10-11",
                                      accession_num=49, owner="Dole", size="medium", type="horse")
        self.horse1.show = self.show
        self.horse2.show = self.show


    
    def test_view_horses_get(self):
        response = self.client.get(reverse('view_horses'))
    
    def test_delete_horse_get(self):
        response = self.client.get(
            reverse('delete_horse', kwargs={"horse_pk": self.horse1.pk}))




    def test_update_horse_add_valid(self):
        
        response = self.client.post(
            reverse('add_horse'), data={'name': "Some Horse Name", 'accession_num': "3DBA", 'coggins_date': self.horse2.coggins_date, 'owner': "Grumpsy", 'type': "Pony",
             'size': "SM",})


    

    def test_update_horse_edit_post(self):
        
        response = self.client.post(
            reverse('edit_horse', kwargs={"horse_pk": self.horse1.pk}), data={'name': "Some Horse Name", 'accession_num': "3DBA", 'coggins_date': self.horse2.coggins_date, 'owner': "Grumpsy", 'type': "Pony",
             'size': "SM",})             

    def test_update_horse_valid(self):
        
        response = self.client.post(
            reverse('add_horse'), data={'name': "Some Horse Name", 'accession_num': "3DBA", 'coggins_date': self.horse2.coggins_date, 'owner': "Grumpsy", 'type': "Pony",
             'size': "SM",})

    def test_update_horse_invalid(self):
        
        response = self.client.post(
            reverse('add_horse'), data={'name': "Some Horse Name", 'accession_num': "3DBA", 'coggins_date': self.horse2.coggins_date, 'owner': "Grumpsy", 'type': "Pony",
             'size': "N/A",})

    def test_get_horse_form_add_get(self):
        response = self.client.get(reverse('get_horse_form'))
    
    def test_get_horse_form_edit_get(self):
        response = self.client.get(reverse('get_horse_form_edit', kwargs={"horse_pk": self.horse1.pk}))


class Labels(TestCase):
    def generate_labels_test(self):
        show = Show.objects.create(date=datetime.datetime.strptime('20190526', "%Y%m%d"), name="Show1", location="Cville", day_of_price=15, pre_reg_price=11)
        try:
            generate_show_labels(show.date)
            self.assertTrue(True)
        except(...):
            self.assertTrue(False)

    def view_generate_labels_test(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.get(reverse('generate_labels', kwargs={'show_date':'2018-12-10'}))
        self.assertTrue(response.status_code == 200)

class ShowViewTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_accepted_get(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.get(reverse('log_in'))

    def test_add_show_get(self):
           show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
           new_division = Division.objects.create(name="division")
           request = HttpRequest()
           client = Client()
           response = client.get(reverse('add_show'))

    def test_add_show_post_error(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.post('/show/add', {'name':'test', 'date':'2018-12-10', 'location':'here', 'day_of_price':10, 'pre_reg_price':5})

    def test_add_show_post_error_blank(self):
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/add', {'name':'', 'date':'', 'location':12, 'day_of_price':10, 'pre_reg_price':5})

    def test_add_show_post(self):
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/add', {'name':'test', 'date':'2018-12-10', 'location':'here', 'day_of_price':10, 'pre_reg_price':5})
        self.assertRedirects(response, '/show/2018-12-10/view')

    def test_view_show(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.get(reverse('view_show', kwargs={'show_date':'2018-12-10'}))

    def test_view_show(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.post(reverse('view_show', kwargs={'show_date': show.date}), data={'num':200})
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

class ComboTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        self.rider = Rider.objects.create(first_name="Anna", last_name="Wu", address="address1", city="cville", state="VA",
                                     zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        self.horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="Horse", size="N/A")
        
        self.horse2 = Horse.objects.create(name="Rubio", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace345", owner="Anna Wu", type="Horse", size="N/A")

        self.horse3 = Horse.objects.create(name="Mykolos", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace345", owner="Anna Wu", type="Horse", size="SM")

        self.combo1 = HorseRiderCombo.objects.create(
            num=200, rider=self.rider, horse=self.horse1, show=self.show)


        self.combo2 = HorseRiderCombo.objects.create(
            num=900, rider=self.rider, horse=self.horse2, show=self.show, is_preregistered=True)

        self.division = Division.objects.create(name="jump", show=self.show)

        self.class1 = Class.objects.create(name="Test", num="1", division=self.division, show=self.show)

        self.class2 = Class.objects.create(name="Test2", num="0", division=self.division, show=self.show)

        self.participation = ClassParticipation.objects.create(participated_class=self.class1, combo=self.combo1)

    def test_calculate_combo_bill_preregistered(self):
        calculate_combo_bill(self.combo2)

    def test_view_combos_get(self):
        response = self.client.get(reverse('view_combos', kwargs={'show_date': self.show.date}))

        
    def test_delete_combo(self):
        response = self.client.get(reverse('delete_combo', kwargs={'combo_pk': self.combo1.pk}))


    def test_add_combo_valid(self):
        response = self.client.post(reverse('add_combo', kwargs={'show_date': self.show.pk}), data={
            'num': 404,
            'rider': self.rider.pk,
            'horse': self.horse3.pk,
            'email': "coudlbyanyting@gmail.com",
            'is_preregistered': True,
            'contact': "Parent"
        })


    def test_add_combo_invalid(self):
        response = self.client.post(reverse('add_combo', kwargs={'show_date': self.show.pk}), data={
            'num': 303,
            'rider': self.rider.pk,
            'horse': self.horse1.pk,
            'email': "coudlbyanyting@gmail.com",
            'is_preregistered': True,
            'contact': "Parent"
        })

    
    def test_edit_combo_valid(self):
        response = self.client.post(reverse('edit_combo', kwargs={'combo_pk': self.combo1.pk}), data={
            'num': 238,
            'rider': self.rider.pk,
            'horse': self.horse1.pk,
            'email': "heyheyhey@gmail.com",
            'is_preregistered': False,
            'contact': "Rider"
        })


    def test_edit_combo_invalid(self):
        response = self.client.post(reverse('edit_combo', kwargs={'combo_pk': self.combo1.pk}), data={
            'num': 909,
            'rider': self.rider.pk,
            'horse': self.horse1.pk,
            'email': "heyheyhe",
            'is_preregistered': True,
            'contact': "Rider"
        })


    def test_view_combo(self):
        response = self.client.get(reverse('view_combo', kwargs={'combo_pk': self.combo1.pk}))

    def test_get_combo_form_combo_exists(self):
        response = self.client.get(reverse('get_combo_form_edit', kwargs={'combo_pk': self.combo1.pk}))


    def test_get_combo_form_combo_nones(self):
        response = self.client.get(reverse('get_combo_form'))




    def test_get_class_in_combo_row_get(self):
        response = self.client.get(reverse('get_class_in_combo_row', kwargs={'participation_pk': self.participation.pk}))


    def test_add_class_to_combo_class_exists_non_duplicate(self):
        response = self.client.post(reverse('add_class_to_combo', kwargs={'combo_pk': self.combo1.pk}), data={'class_num': 0})


    def test_add_class_to_combo_class_exists_duplicate(self):
        response = self.client.post(reverse('add_class_to_combo', kwargs={'combo_pk': self.combo1.pk}), data={'class_num': 1})


    def test_add_class_to_combo_class_does_not_exist(self):
        response = self.client.post(reverse('add_class_to_combo', kwargs={'combo_pk': self.combo1.pk}), data={'class_num': 300})


    def test_delete_participation_part_exists(self):
        response = self.client.get(reverse('delete_participation', kwargs={'combo_pk': self.combo1.pk, 'class_pk': self.class1.pk}))


    def test_delete_participation_part_does_not_exist(self):
        response = self.client.get(reverse('delete_participation', kwargs={'combo_pk': self.combo1.pk, 'class_pk': self.class2.pk}))


    


class DivisionsTestCases(TestCase):
    def test_add_division(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/add', {'name':'jumper'})

    def test_add_division_error(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        self.client.login(username='john', password='johnpassword')
        d1 = Division.objects.create(name="jumper", show=show)
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/add', {'name':'jumper'})

    def test_add_division_get(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get(reverse('add_division', kwargs={'show_date':'2018-12-10'}))


class RejectedLoginTest(TestCase):
    def test_rejected_get(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        request = HttpRequest()
        response = self.client.get(reverse('log_in'))

class RankTestCases(TestCase):
    def test_rank_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/1/rank', {'first':100, 'second':200, 'third':300, 'fourth':400, 'fifth':500, 'sixth':600})

    def test_rank_class_post(self):
        self.client.login(username='john', password='johnpassword')
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        horse2 = Horse.objects.create(name="Joey", coggins_date=datetime.datetime.strptime(
            '20130522', "%Y%m%d").date(), accession_num="a33123", owner="A Wu", type="horse", size="N/A")
        rider1 = Rider.objects.create(first_name="Anna",last_name= "Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=200, rider=rider1, horse=horse1, show=show)
        combo2 = HorseRiderCombo.objects.create(
            num=300, rider=rider1, horse=horse2, show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        class_participation = ClassParticipation.objects.create(participated_class=c1, combo=combo1)
        class_participation = ClassParticipation.objects.create(participated_class=c1, combo=combo2)
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/1/rank', {'first':200, 'second':300})

    def test_rank_class_get(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get('/show/2018-12-10/division/1/class/1/rank')

    def test_rank_class_duplicates(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/1/rank', {'first':100, 'second':100, 'third':300, 'fourth':400, 'fifth':500, 'sixth':600})

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

class DivisionsTestCase(TestCase): #sprint 11 unit tests shannon
    def test_delete_division(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get('/show/2018-12-10/division/1/delete')

    def test_edit_division(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get('/show/2018-12-10/division/1/edit')

    def test_edit_division_post(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/edit', {'change_name_to':'equitation'})

class RiderTestCase(TestCase): #sprint 11 unit tests shannon
    def test_add_rider(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        rider1 = Rider.objects.create(first_name="Anna",last_name= "Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/rider/add', {'first_name': "Anna", 'last_name':"Wu", 'address': "address1", 'city': "cville", 'state': "VA", 'zip_code': 22033, 'email': "thisisarandomemail@gmail.com",
                  'adult': True, 'birth_date': datetime.datetime.strptime('20040122', "%Y%m%d").date(), 'member_VHSA': True, 'county': "county"})

    def test_edit_rider(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        rider1 = Rider.objects.create(first_name="Anna",last_name= "Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/rider/1/edit', {'first_name': "Anna", 'last_name':"Wu", 'address': "address1", 'city': "cville", 'state': "VA", 'zip_code': 22033, 'email': "thisisarandomemail@gmail.com",
                  'adult': True, 'birth_date': datetime.datetime.strptime('20040122', "%Y%m%d").date(), 'member_VHSA': True, 'county': "county"})


class ClassTestCase(TestCase):
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
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/add', {'num':1, 'name':'jumper'})

    def test_add_class_error(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/add', {'num':1, 'name':'jumper'})

    def test_add_class_get(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get(reverse('add_class', kwargs={'show_date':'2018-12-10','division_id':d1.id}))

    def test_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get('/show/2018-12-10/division/1/')

    def test_delete_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get('/show/2018-12-10/division/1/class/1/delete')

    def test_delete_class_post(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        c2 = Class.objects.create(name="Test2", num="2", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get('/show/2018-12-10/division/1/class/1/delete')

class DivisionScoreTestCase(TestCase):
    def test_division_scores(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get('/show/2018-12-10/division/1/scores')

    def test_add_division_scores(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        self.client.login(username='john', password='johnpassword')
        d1 = Division.objects.create(name="jumper", show=show)
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/scores', {'champion':100, 'champion_pts':10, 'champion_reserve':200, 'champion_reserve_pts':6})

class AddClassToDivisionTestCase(TestCase):
    def test_add_class_division_post(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        self.client.login(username='john', password='johnpassword')
        d1 = Division.objects.create(name="jumper", show=show)
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/', {'name':'jumper kid', 'num':1})

    def test_add_class_division_post_error(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        self.client.login(username='john', password='johnpassword')
        d1 = Division.objects.create(name="jumper", show=show)
        c1 = Class.objects.create(name="jumper kid", num="1", division=d1, show=show)
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/', {'name':'jumper kid', 'num':1})


class TestViewClassTestCase(TestCase):

    def test_view_class_error_duplicate(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        rider1 = Rider.objects.create(first_name="Anna",last_name= "Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=200, rider=rider1, horse=horse1, show=show)
        class_participation = ClassParticipation.objects.create(participated_class=c1, combo=combo1)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/1/', {'num':'200'})

    def test_view_class_error_dne(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/1/', {'num':'400'})

    def test_view_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="N/A")
        rider1 = Rider.objects.create(first_name="Anna",last_name= "Wu", address="address1", city="cville", state="VA",
                                      zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=200, rider=rider1, horse=horse1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.post('/show/2018-12-10/division/1/class/1/', {'num':'200'})
    def test_view_class_get(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Test", num="1", division=d1, show=show)
        self.client.login(username='john', password='johnpassword')
        request = HttpRequest()
        response = self.client.get('/show/2018-12-10/division/1/class/1/')

    
class AddDuplicateClass(TestCase):
    def test_failed_add_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Class1", num="1", division=d1, show=show)
        with self.assertRaises(IntegrityError):
            Class.objects.create(name="Class1", num="1", division=d1, show=show)

    @contextmanager
    def assertNotRaises(self, exc_type):
        try:
            yield None
        except exc_type:
            raise self.failureException('{} raised'.format(exc_type))

    def test_add_unique_class(self):
        show = Show.objects.create(name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        d1 = Division.objects.create(name="jump", show=show)
        c1 = Class.objects.create(name="Class1", num="1", division=d1, show=show)
        with self.assertNotRaises(IntegrityError):
            Class.objects.create(name="Class2", num="2", division=d1, show=show)

class ChangedRiderModels(TestCase):
    def test_valid_address(self):
        form = RiderForm(data={'first_name':'Rider1','last_name':'test', 'address':'', 'city':'', 'state':"VA",
                                      'zip_code':'22903', 'email':'aw@email.com', 'adult':'False',
                                      'birth_date':'2008-12-10'})
        self.assertTrue(form.is_valid())

    def test_invalid_address(self):
        form = RiderForm(data={'first_name':'','last_name':'', 'address':'', 'city':'', 'state':"VA",
                                      'zip_code':'22903', 'email':'aw@email.com', 'adult':'False',
                                      'birth_date':'2008-12-10'})
        self.assertFalse(form.is_valid())

class CheckChampion(TestCase):
    def test_champion_horse(self):
        show = Show.objects.create(
            name="test", date="2018-12-10", location="here", day_of_price=10, pre_reg_price=5)
        division = Division.objects.create(name="division")
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        rider1 = Rider.objects.create(first_name="Anna", last_name ="Wu", address="address1", city="cville", state="VA",zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo1 = HorseRiderCombo.objects.create(
            num=200, rider=rider1, horse=horse1, show = show)
        division.champion = horse1.name
        self.assertTrue(division.champion == "Ruby")


class CheckReserve(TestCase):
    def test_reserve_horse(self):
        show = Show.objects.create(
            name="show1", date="2019-12-10", location="cville", day_of_price=15, pre_reg_price=10)
        division = Division.objects.create(name="division")
        horse = Horse.objects.create(name="Pikachu", coggins_date=datetime.datetime.strptime(
            '20110522', "%Y%m%d").date(), accession_num="que847", owner="Anna Wu", type="pony", size="small")
        rider = Rider.objects.create(first_name="Anna", last_name ="Wu", address="address1", city="cville", state="VA",zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo = HorseRiderCombo.objects.create(
            num=200, rider=rider, horse=horse, show = show)
        division.champion_reserve = horse.name
        self.assertTrue(division.champion_reserve == "Pikachu")

class StrTestMethods(TestCase):
    def test_division_model(self):
        show = Show.objects.create(
            name="show1", date="2019-12-10", location="cville", day_of_price=15, pre_reg_price=10)
        division = Division.objects.create(name="division", show=show)
        self.assertIsNotNone(str(division))

    def test_class_model(self):
        c1 = Class.objects.create(name="Class1", num="1")
        self.assertIsNotNone(str(c1))

    def test_horse_model(self):
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        self.assertIsNotNone(str(horse1))

    def test_horse_model(self):
        horse1 = Horse.objects.create(name="Ruby", coggins_date=datetime.datetime.strptime(
            '20100522', "%Y%m%d").date(), accession_num="ace123", owner="Anna Wu", type="horse", size="NA")
        self.assertIsNotNone(str(horse1))

    def test_rider_model(self):
        rider = Rider.objects.create(first_name="Anna", last_name ="Wu", address="address1", city="cville", state="VA",zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        self.assertIsNotNone(str(rider))

    def test_combo_model(self):
        show = Show.objects.create(
            name="show1", date="2019-12-10", location="cville", day_of_price=15, pre_reg_price=10)
        division = Division.objects.create(name="division")
        horse = Horse.objects.create(name="Pikachu", coggins_date=datetime.datetime.strptime(
            '20110522', "%Y%m%d").date(), accession_num="que847", owner="Anna Wu", type="pony", size="small")
        rider = Rider.objects.create(first_name="Anna", last_name ="Wu", address="address1", city="cville", state="VA",zip_code="22903", email="aw@email.com", adult=False, birth_date=datetime.datetime.strptime('20040122', "%Y%m%d").date())
        combo = HorseRiderCombo.objects.create(
            num=200, rider=rider, horse=horse, show = show)
        self.assertIsNotNone(str(combo))
