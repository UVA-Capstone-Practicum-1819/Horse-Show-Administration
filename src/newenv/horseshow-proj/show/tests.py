from django.test import TestCase

from show.models import Show, Rider, Horse, Classes
from django.contrib.auth.forms import UserCreationForm

# Create your tests here.


class ShowTestCase(TestCase):
    def create_show(self, title="test", body="test for a show"):
        return Show.objects.create(show_name="Boopalooza", show_date="10/02/2018", show_location="Pony Barn")

    def test_show_creation(self):
        testshow = self.create_show()
        self.assertTrue(isinstance(testshow, Show))


class ShowTestIntCase(TestCase):
    def create_show(self, title="test", body="test for a show"):
        return Show.objects.create(show_name="Boopalooza", show_date=10022018, show_location="Pony Barn")

    def test_show_creation(self):
        testshow = self.create_show()
        self.assertTrue(isinstance(testshow, Show))


class RiderTestCase(TestCase):
    def create_rider(self, title="test", body="test for rider"):
        return Rider.objects.create(name="Lauren", address="234 cotton lane", age=12, email="sdd3ee@virginia.edu")

    def test_rider_creation(self):
        testrider = self.create_rider()
        self.assertTrue(isinstance(testrider, Rider))


class RiderTestFailCase(TestCase):
    def create_rider(self, title="test", body="test for rider"):
        try:
            rider = Rider.objects.create(
                name="Lauren", address="234 cotton lane", age="thirteen", email="sdd3ee@virginia.edu")
        except:
            print("this is an invalid insert")
            return 0
        return rider

    def test_rider_creation(self):
        testrider = self.create_rider()
        self.assertFalse(isinstance(testrider, Rider))


class HorseTestCase(TestCase):
    def create_horse(self, title="test", body="test for horse"):
        return Horse.objects.create(name="Smokey Mountain", barn_name="Smokey", age=10, coggins=10102, owner="Tina", size="pony", type="shetland")

    def test_horse_creation(self):
        testhorse = self.create_horse()
        self.assertTrue(isinstance(testhorse, Horse))


class LoginTestCase(TestCase):
    """
    test cases for logging in and signing up (users)

    can use c = Client() for creating a client and

    response = c.post(url, context_params) to post data to the url page

    response = c.get(url) to get the page (doing c.get(url, follow=True) allows you to get the redirect chain via response.redirect_chain )

    also

    c.login(username='fred', password='secret') to login users (returns True if successful)

    response.context[key] to get the context value for the key
    """

    def signup_with_incorrect_input(self):
        data = {'username': "testexampleuser",
                'password1': "testuserpassword", 'password2': "testuserpasswordwrong"}
        form = UserCreationForm(data=data)
        self.assertTrue(form.is_valid())
