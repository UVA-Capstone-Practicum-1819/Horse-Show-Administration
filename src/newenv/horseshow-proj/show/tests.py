from django.test import TestCase, Client
from show.models import Show, Rider, Horse, Classes
from show.forms import ShowForm, RiderForm, HorseForm, HorseSelectForm, RiderSelectForm, ShowSelectForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from show import models


# Create your tests here.


class ShowTestCase(TestCase):
    def create_show(self, title="test", body="test for a show"):
        return Show.objects.create(show_name="Boopalooza", show_date="2018-10-07", show_location="Pony Barn")

    def test_show_creation(self):
        testshow = self.create_show()
        self.assertTrue(isinstance(testshow, Show))


class ShowFormTestCase(TestCase):
    def test_showForm_validsdashes(self):
        form = ShowForm(data={'show_name':'Boopalooza', 'show_date':'2018-10-02', 'show_location':'Pony Barn'})
        self.assertTrue(form.is_valid())

    def test_showForm_validslashes(self):
        form = ShowForm(data={'show_name':'Boopalooza', 'show_date':'10/12/2018', 'show_location':'Pony Barn'})
        self.assertTrue(form.is_valid())

    def test_showForm_invaliddatenomarks(self):
        form = ShowForm(data={'show_name':'Balooza', 'show_date':'20191003', 'show_location':'Pony'})
        self.assertFalse(form.is_valid())

    def test_showForm_invalidorder(self):
        form = ShowForm(data={'show_name':'Boopalooza', 'show_date':'10-30-3029', 'show_location':'Pony Barn'})
        self.assertFalse(form.is_valid())

    def test_showForm_invalidstring(self):
        form = ShowForm(data={'show_name':'Balooza', 'show_date':'30th of September', 'show_location':'Pony'})
        self.assertFalse(form.is_valid())

    def test_showForm_invalidemptyfields(self):
        form = ShowForm(data={'show_name':'', 'show_date':'', 'show_location':''})
        self.assertFalse(form.is_valid())

    def test_ShowSelectForm_invalid(self):
        form = ShowSelectForm(data={'name': ""})
        self.assertFalse(form.is_valid())

class ShowTestIntCase(TestCase):
    def create_show(self, title="test", body="test for a show"):
        return Show.objects.create(show_name="Boopalooza", show_date="2019-10-03", show_location="Pony Barn")

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

class HorseTestCase(TestCase):
    # def setup(self):
    #     user = User.objects.create(username='user')
    #     user.set_password('password')
    #     user.save()
    def create_horse(self, title="test", body="test for horse"):
        return Horse.objects.create(name="Smokey Mountain", barn_name="Smokey", age=10, coggins=10102, owner="Tina", size="pony", type="shetland")

    def test_horse_creation(self):
        testhorse = self.create_horse()
        self.assertTrue(isinstance(testhorse, Horse))

    # def test_horse_page(self):
    #     c = Client()
    #     logged_in = c.login(username='user', password='password')
    #     response = self.client.post('show/horse/new', follow=True)
    #     self.assertEqual(response.status_code, 200)

    def test_horse_Invalidform(self):
        form_vals= {'name': 'Misty', 'barn_name': 'Misty', 'age': '4', 'coggins': '12345', 'owner':'Al', 'size':'pony'}
        form= HorseForm(data=form_vals)
        self.assertFalse(form.is_valid())
    def test_horse_Invalidform2(self):
            form_vals= {'name': '', 'barn_name': 'Misty', 'age': '4', 'coggins': '12345', 'owner':'Al', 'size':'pony'}
            form= HorseForm(data=form_vals)
            self.assertFalse(form.is_valid())

    def test_horse_Validform(self):
        form_vals= {'name': 'Misty', 'barn_name': 'Misty', 'age': '4', 'coggins': '12345', 'owner':'Al', 'size':'pony', 'type':'shetland'}
        form= HorseForm(data=form_vals)
        self.assertTrue(form.is_valid())

    def test_horse_ValidformInt(self):
        values= {'name': 'Boi', 'barn_name': 'Boiiii', 'age': 5, 'coggins': 12345, 'owner':'Joe', 'size':'horse', 'type':'Thoroughbred'}
        form= HorseForm(data=values)
        self.assertTrue(form.is_valid())

class HorseSelectCase(TestCase):
    # def setup(self):
    #     user = User.objects.create(username='user')
    #     user.set_password('password')
    #     user.save()
    def create_horse(self, title="test", body="test for horse"):
        return Horse.objects.create(name = "Misty", barn_name="Misty", age=4, coggins=12345, owner="Tina", size="pony", type="shetland")
    # def test_horse_select_page(self):
    #     c = Client()
    #     logged_in = c.login(username='user', password='password')
    #     response = self.client.post('show/horse-autocomplete/', follow=True)
    #     self.assertEqual(response.status_code, 200)
    def test_horse_select_Invalidform2(self):
        form_vals= {}
        form= HorseSelectForm(data=form_vals)
        self.assertFalse(form.is_valid())

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


class HorseRiderComboTest(TestCase):
    def setUp(self):
        horse1 = Horse.objects.create(name = "Misty", barn_name="Misty", age=4, coggins=12345, owner="Tina", size="pony", type="shetland")
        horse2 = Horse.objects.create(name = "Brock", barn_name="Brock", age=5, coggins=73854, owner="Brock has no Owner!", size="unicorn", type="unicorn")
        horse3 = Horse.objects.create(name = "Ash", barn_name="Ash", age=5, coggins=747, owner="May", size="pony", type="pony")
        horse4 = Horse.objects.create(name = "Pikachu", barn_name="Pikachu", age=1, coggins=8736, owner="Ash", size="mouse", type="mouse")

        rider1 = Rider.objects.create(name = "Tarun", address="116 Chelsea Dr", age=22, email="ts4pe@virginia.edu")
        rider2 = Rider.objects.create(name = "Yunzhe", address="idunno ln.", age=22, email="ts4pe@virginia.edu")
        rider3 = Rider.objects.create(name = "Shannon", address="sfds", age=22, email="ts4pe@virginia.edu")




# class ComboTestCase(TestCase):
#     def create_combo(self, title="test", body="test for add combo"):
#         return Combo.objects.create(combo='234', ridername="Richard Lee", horsename = "Jenny", owner="John Doe")

#     def test_create_combo(self):
#         test_combo = self.create_combo()
#         self.assertTrue(isinstance(test_combo, Combo))

# class ComboIntTestCase(TestCase):
#     def create_combo(self, title="test", body="test for add int combo"):
#         return Combo.objects.create(combo=564, ridername="Jane Doe", horsename = "Toby", owner="Oliver Parker")

#     def test_create_combo(self):
#         test_combo = self.create_combo()
#         self.assertTrue(isinstance(test_combo, Combo))

# class ComboRandomTestCase(TestCase):
#     def create_combo(self, title="test", body="test for add random combo"):
#         return Combo.objects.create(combo= models.random_string(), ridername="Jane Doe", horsename = "Toby", owner="Oliver Parker")

#     def test_create_combo(self):
#         test_combo = self.create_combo()
#         self.assertTrue(isinstance(test_combo, Combo))

# class RandomCombinationTestCase1(TestCase):
#     def generate_random_three_digit_int(self, title="test", body="test for three digit integer"):
#         return models.random_string()
#     def test_generate_random(self):
#         for i in range (10):
#             test_random_int = self.generate_random_three_digit_int()
#             self.assertTrue(len(test_random_int), 3)

# class RandomCombinationTestCase2(TestCase):
#     def generate_random_int(self, title="test", body="test for integer range"):
#         return models.random_string()
#     def test_generate_random(self):
#         for i in range (10):
#             test_random_int = self.generate_random_int()
#             self.assertTrue(0 <= int(test_random_int) <= 999)
