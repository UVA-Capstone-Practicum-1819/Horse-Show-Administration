from django.test import TestCase, Client
from show.models import Show, Rider, Horse
from show.forms import ShowForm, RiderForm, HorseForm, HorseSelectForm, RiderSelectForm
from django.contrib.auth.models import User

class ShowTestCase(TestCase):
    def create_show(self, title="test", body="test for a show"):
        return Show.objects.create(show_name = "Boopalooza", show_date="10/02/2018", show_location="Pony Barn")

    def test_show_creation(self):
        testshow = self.create_show()
        self.assertTrue(isinstance(testshow, Show))

class ShowTestIntCase(TestCase):
    def create_show(self, title="test", body="test for a show"):
        return Show.objects.create(show_name = "Boopalooza", show_date=10022018, show_location="Pony Barn")

    def test_show_creation(self):
        testshow = self.create_show()
        self.assertTrue(isinstance(testshow, Show))

class RiderTestCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()

    def create_rider(self, title="test", body="test for rider"):
        return Rider.objects.create(name = "Lauren", address="234 cotton lane", age=12, email="sdd3ee@virginia.edu")

    def test_rider_creation(self):
        testrider = self.create_rider()
        self.assertTrue(isinstance(testrider, Rider))

    def test_rider_page(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        response = self.client.post('show/rider/new', follow=True)
        self.assertEqual(response.status_code, 200)

class RiderTestFailCase(TestCase):
    def create_rider(self, title="test", body="test for rider"):
        try:
            rider = Rider.objects.create(name = "Lauren", address="234 cotton lane", age="thirteen", email="sdd3ee@virginia.edu")
        except:
            print("this is an invalid insert")
            return 0
        return rider

    def test_rider_creation(self):
        testrider = self.create_rider()
        self.assertFalse(isinstance(testrider, Rider))

# redirect from rider select to horse_select
# redir from ridernew to HorseSelect
# redir index to RiderSelect

#  if ridernew fails
class RiderFormsTest(TestCase):
    def test_RiderForm_valid(self):
        form = RiderForm(data={'name': "sarah", 'address': "address1", 'age': 9, 'email': "email@123.com"})
        self.assertTrue(form.is_valid())

    def test_RiderForm_invalid(self):
        form = RiderForm(data={'name': "", 'address': "", 'age': 9, 'email': ""})
        self.assertFalse(form.is_valid())

    # def test_RiderSelectForm_valid(self):
    #     form = RiderSelectForm(data={'name': "shiv"})
    #     self.assertTrue(form.is_valid())
    def test_RiderSelectForm_invalid(self):
        form = RiderSelectForm(data={'name': ""})
        self.assertFalse(form.is_valid())

    def test_RiderSelectPage(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        response = self.client.post('rider/horse-autocomplete/', follow=True)
        self.assertEqual(response.status_code, 200)


# class RedirectSelectForms(TestCase):
#     c = Client()
#     c.login(username='user', password='password')
#     response = c.get(reverse('pledges:home_group', kwargs={'group_id': 100}), follow=True)
#
#     SimpleTestCase.assertRedirects(response, reverse('pledges:home'))



class HorseTestCase(TestCase):
    def create_horse(self, title="test", body="test for horse"):
        return Horse.objects.create(name = "Smokey Mountain", barn_name="Smokey", age=10, coggins=10102, owner="Tina", size="pony", type="shetland")

    def test_horse_creation(self):
        testhorse = self.create_horse()
        self.assertTrue(isinstance(testhorse, Horse))
