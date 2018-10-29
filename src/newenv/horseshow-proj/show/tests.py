from django.test import TestCase, Client

from show.models import Show, Rider, Horse, Classes
from show.forms import ShowForm, RiderForm, HorseForm, HorseSelectForm
from django.contrib.auth.models import User
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
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()
    def create_horse(self, title="test", body="test for horse"):
        return Horse.objects.create(name="Smokey Mountain", barn_name="Smokey", age=10, coggins=10102, owner="Tina", size="pony", type="shetland")

    def test_horse_creation(self):
        testhorse = self.create_horse()
        self.assertTrue(isinstance(testhorse, Horse))

    def test_horse_page(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        response = self.client.post('show/horse/new', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_horse_Invalidform(self):
        form_vals= {'name': 'Misty', 'barn_name': 'Misty', 'age': '4', 'coggins': '12345', 'owner':'Al', 'size':'pony'}
        form= HorseForm(data=form_vals)
        self.assertFalse(form.is_valid())

    def test_horse_Validform(self):
        form_vals= {'name': 'Misty', 'barn_name': 'Misty', 'age': '4', 'coggins': '12345', 'owner':'Al', 'size':'pony', 'type':'shetland'}
        form= HorseForm(data=form_vals)
        self.assertTrue(form.is_valid())

class HorseSelectCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()
    def create_horse(self, title="test", body="test for horse"):
        return Horse.objects.create(name = "Misty", barn_name="Misty", age=4, coggins=12345, owner="Tina", size="pony", type="shetland")
    def test_horse_select_page(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        response = self.client.post('show/horse-autocomplete/', follow=True)
        self.assertEqual(response.status_code, 200)
    def test_horse_select_Invalidform(self):
        form_vals= {'name':''}
        form= HorseSelectForm(data=form_vals)
        self.assertFalse(form.is_valid())

class ClassTestCase(TestCase):
    def test_name(self):
        self.assertEqual(Classes.CLASS_CHOICES[0], ('cwu', '1. California Warm Up'))

    def test_check_type(self):
        self.assertTrue(isinstance(Classes.CLASS_CHOICES[0], tuple))

    def test_index(self):
        self.assertEqual(Classes.CLASS_CHOICES.index(('pef', '35. Pony Equitation on the Flat')), 34)

    def test_length(self):
        self.assertEqual(len(Classes.CLASS_CHOICES), 48)

    def test_selected(self):
        self.assertFalse(Classes.CLASS_CHOICES[0] == 'on')

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

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(self.credentials)
        self.client = Client()

    """ using incorrect credentials; should not make valid form """

    def signup_with_incorrect_input(self):
        data = {'username': "testexampleuser",
                'password1': "testuserpassword", 'password2': "testuserpasswordwrong"}
        form = UserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    """ using correct credentials; should make valid form """

    def signup_with_correct_input(self):
        data = {'username': "testexampleuser",
                'password1': "testuserpassword", 'password2': "testuserpassword"}
        form = UserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    """ using incorrect credentials; should not make user logged in (active) """

    def login_with_incorrect_input(self):
        data = {'username': "testuser",
                'password1': "secretwrong", }
        response = self.client.post(reverse('login'), data)

        self.assertFalse(response.context['user'].is_active)

    """ using correct credentials; should make user logged in (active) """

    def login_with_correct_input(self):
        data = {'username': "testuser",
                'password1': "secret", }
        response = self.client.post(reverse('login'), data)

        self.assertTrue(response.context['user'].is_active)

    """ log out the user, should be inactive """

    def logout(self):
        self.client.get(reverse('logout'))
        self.assertFalse(response.context['user'].is_active)
