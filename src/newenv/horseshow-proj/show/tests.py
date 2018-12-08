from django.test import TestCase, Client
from show.models import Show, Rider, Horse, Classes
from show.models import *
from show.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from show import models
# Create your tests here.

class ShowTestCase(TestCase):
    def create_show(self, title="test", body="test for a show"):
        return Show.objects.create(name="Boopalooza", date="2018-10-07", location="Pony Barn")

    def test_show_creation(self):
        testshow = self.create_show()
        self.assertTrue(isinstance(testshow, Show))

class ShowFormTestCase(TestCase):
    # def test_showForm_validsdashes(self):
    #     form = ShowForm(data={'name':'Boopalooza', 'date':'2018-10-02', 'location':'Pony Barn'})
    #     self.assertTrue(form.is_valid())
    #
    # def test_showForm_validslashes(self):
    #     form = ShowForm(data={'name':'Boopalooza', 'date':'10/12/2018', 'location':'Pony Barn'})
    #     self.assertTrue(form.is_valid())

    def test_showForm_invaliddatenomarks(self):
        form = ShowForm(data={'name':'Balooza', 'date':'20191003', 'location':'Pony'})
        self.assertFalse(form.is_valid())

    def test_showForm_invalidorder(self):
        form = ShowForm(data={'name':'Boopalooza', 'date':'10-30-3029', 'location':'Pony Barn'})
        self.assertFalse(form.is_valid())

    def test_showForm_invalidstring(self):
        form = ShowForm(data={'name':'Balooza', 'date':'30th of September', 'location':'Pony'})
        self.assertFalse(form.is_valid())

    def test_showForm_invalidemptyfields(self):
        form = ShowForm(data={'name':'', 'date':'', 'location':''})
        self.assertFalse(form.is_valid())

    def test_ShowSelectForm_invalid(self):
        form = ShowSelectForm(data={'name': ""})
        self.assertFalse(form.is_valid())

class ShowTestIntCase(TestCase):
    def create_show(self, title="test", body="test for a show"):
        return Show.objects.create(name="Boopalooza", date="2019-10-03", location="Pony Barn")

    def test_show_creation(self):
        testshow = self.create_show()
        self.assertTrue(isinstance(testshow, Show))

class BillTests(TestCase):
    def test_billpagesetUp(self):
        horse1 = Horse.objects.create(name = "Misty", barn_name="Misty", age=4, coggins=12345, owner="Tina", size="pony", type="shetland")
        # horse2 = Horse.objects.create(name = "Brock", barn_name="Brock", age=5, coggins=73854, owner="Brock has no Owner!", size="unicorn", type="unicorn")
        # horse3 = Horse.objects.create(name = "Ash", barn_name="Ash", age=5, coggins=747, owner="May", size="pony", type="pony")
        # horse4 = Horse.objects.create(name = "Pikachu", barn_name="Pikachu", age=1, coggins=8736, owner="Ash", size="mouse", type="mouse")
        rider1 = Rider.objects.create(name = "Tarun", address="116 Chelsea Dr", age=22, email="ts4pe@virginia.edu")
        # rider2 = Rider.objects.create(name = "Yunzhe", address="idunno ln.", age=22, email="ts4pe@virginia.edu")
        # rider3 = Rider.objects.create(name = "Shannon", address="sfds", age=22, email="t4pe@virginia.edu")
        c = Classes.objects.create(name="Test", number="1")
        c2 = Classes.objects.create(name="Test2", number="2")
        hrc1 = HorseRiderCombo.objects.create(num = 12, rider = rider1, horse = horse1)
        hrc1.classes.add(c)
        hrc1.classes.add(c2)

    # def test_numclasses(self):
        self.assertEqual(hrc1.classes.count(), 2, "correct num classes")
        hrc1.classes.remove(c)
        self.assertEqual(hrc1.classes.count(), 1, "correct num classes after remove")



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
        form = RiderForm(data={'name': "x", 'address': "xx", 'age': 9, 'email': "x@x.com"})
        self.assertTrue(form.is_valid())

    def test_RiderForm_invalidname(self):
        form = RiderForm(data={'name': "", 'address': "xx", 'age': 9, 'email': "x@x.com"})
        self.assertFalse(form.is_valid())
    def test_RiderForm_invalidaddress(self):
        form = RiderForm(data={'name': "x", 'address': "", 'age': 9, 'email': "x@x.com"})
        self.assertFalse(form.is_valid())
    def test_RiderForm_invalidagetype(self):
        form = RiderForm(data={'name': "x", 'address': "xx", 'age': "xxx", 'email': "x@x.com"})
        self.assertFalse(form.is_valid())
    def test_RiderForm_invalidageempty(self):
        form = RiderForm(data={'name': "x", 'address': "xx", 'age': '', 'email': "x@x.com"})
        self.assertFalse(form.is_valid())
    def test_RiderForm_invalidagerange(self):
        form = RiderForm(data={'name': "x", 'address': "xx", 'age': -1, 'email': "x@x.com"})
        self.assertFalse(form.is_valid())
    def test_RiderForm_invalidemail(self):
        form = RiderForm(data={'name': "x", 'address': "xx", 'age': 9, 'email': "xx.com"})
        self.assertFalse(form.is_valid())
    def test_RiderForm_invalidemailnodot(self):
        form = RiderForm(data={'name': "x", 'address': "xx", 'age': 9, 'email': "xx@com"})
        self.assertFalse(form.is_valid())
    def test_RiderForm_invalidemailempty(self):
        form = RiderForm(data={'name': "x", 'address': "xx", 'age': 9, 'email': ""})
        self.assertFalse(form.is_valid())
    def test_RiderSelectForm_valid(self):
        rider2 = Rider.objects.create(name = "Test", address="idunno ln.", age=22, email="ts4pe@virginia.edu")
        values = {'name': "Test"}
        form = RiderSelectForm(data=values)
        self.assertTrue(form.is_valid)
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
    def test_HorseSelectForm_valid(self):
        # rider2 = Horse.objects.create(name = "Misty", barn_name="Misty", age=4, coggins=12345, owner="Tina", size="pony", type="shetland")
        values = {'name': "Misty"}
        form = HorseSelectForm(data=values)
        self.assertTrue(form.is_valid)

    def test_horse_select_Invalidform2(self):
        form_vals= {}
        form= HorseSelectForm(data=form_vals)
        self.assertFalse(form.is_valid())

    def test_horse_select_Invalidform(self):
        form_vals= {'name':''}
        form= HorseSelectForm(data=form_vals)
        self.assertFalse(form.is_valid())

# class ClassTestCase(TestCase):
#     def test_name(self):
#         self.assertEqual(Classes.CLASS_CHOICES[0], ('cwu', '1. California Warm Up'))

#     def test_check_type(self):
#         self.assertTrue(isinstance(Classes.CLASS_CHOICES[0], tuple))

#     def test_index(self):
#         self.assertEqual(Classes.CLASS_CHOICES.index(('pef', '35. Pony Equitation on the Flat')), 34)

#     def test_length(self):
#         self.assertEqual(len(Classes.CLASS_CHOICES), 48)

#     def test_selected(self):
#         self.assertFalse(Classes.CLASS_CHOICES[0] == 'on')

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
        data = {'username': "testexampleuser", 'password1': "testuserpassword", 'password2': "testuserpassword"}
        form = UserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    """ using incorrect credentials; should not make user logged in (active) """
    def login_with_incorrect_input(self):
        data = {'username': "testuser", 'password1': "secretwrong", }
        response = self.client.post(reverse('login'), data)
        self.assertFalse(response.context['user'].is_active)

    """ using correct credentials; should make user logged in (active) """
    def login_with_correct_input(self):
        data = {'username': "testuser", 'password1': "secret", }
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


class DivisionsTest(TestCase):
    def test_create_division(self):
        div1 = Division.objects.create(name="Division 1", number="1")
        self.assertTrue(isinstance(div1, Division))

    def test_DivisionSelectPage(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        response = self.client.post('division/division-autocomplete/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_division(self):
        form_vals = {'name': '', 'number': '5'}
        form = DivisionForm(data=form_vals)
        self.assertFalse(form.is_valid())

    # def test_valid_division(self):
    #     form_vals = {'name': 'div example', 'number': '5'}
    #     form = DivisionForm(data=form_vals)
    #     self.assertTrue(form.is_valid())

    def test_invalid_division_select(self):
        form_vals = {'name': ''}
        form = DivisionSelectForm(data=form_vals)
        self.assertFalse(form.is_valid())

class ComboSelect(TestCase):
    def test_comboselectvalid(self):
        horse1 = Horse.objects.create(name = "Misty", barn_name="Misty", age=4, coggins=12345, owner="Tina", size="pony", type="shetland")
        rider1 = Rider.objects.create(name = "Tarun", address="116 Chelsea Dr", age=22, email="ts4pe@virginia.edu")
        c = Classes.objects.create(name="Test", number="1")
        c2 = Classes.objects.create(name="Test2", number="2")
        hrc1 = HorseRiderCombo.objects.create(num = 12, rider = rider1, horse = horse1)
        hrc1.classes.add(c)
        values = {'num': 12}
        form = ClassSelectForm(data=values)
        self.assertTrue(form.is_valid)
    def test_comboselectinvalid(self):
        horse1 = Horse.objects.create(name = "Misty", barn_name="Misty", age=4, coggins=12345, owner="Tina", size="pony", type="shetland")
        rider1 = Rider.objects.create(name = "Tarun", address="116 Chelsea Dr", age=22, email="ts4pe@virginia.edu")
        c = Classes.objects.create(name="Test", number="1")
        c2 = Classes.objects.create(name="Test2", number="2")
        hrc1 = HorseRiderCombo.objects.create(num = 12, rider = rider1, horse = horse1)
        hrc1.classes.add(c)
        values = {'num': 12}
        form = ClassSelectForm(data=values)
        self.assertFalse(form.is_valid())


class ClassesTest(TestCase):
    def test_create_class(self):
        c = Classes.objects.create(name="Test", number="1")
        self.assertTrue(isinstance(c, Classes))

    def test_invalid_class_create(self):
        form_values = {'class_name': 'test', 'class_number':''}
        form = ClassForm(data=form_values)
        self.assertFalse(form.is_valid())

    def test_class_select_form(self):
        c = Classes.objects.create(name="Test", number="1")
        values = {'name': "Test"}
        form = ClassSelectForm(data=values)
        self.assertTrue(form.is_valid)

class AddDivToShowTest(TestCase):
    def test_add_division(self):
        show = Show.objects.create(name="test", date="11/11/2018", location="here")
        division = Division.objects.create(name="div", number=1)
        show.divisions.add(division)
        self.assertTrue(show.divisions.all()[0]==division)

    def test_duplicate_division(self):
        show = Show.objects.create(name="test", date="11/11/2018", location="here")
        division = Division.objects.create(name="div", number=1)
        show.divisions.add(division)
        show.divisions.add(division)
        self.assertTrue(len(show.divisions.all())==1)

##added division failures

class AddDivFailures(TestCase):
    def test_addDivision_noname(self):
        form = ShowForm(data={'name':'', 'number':'201'})
        self.assertFalse(form.is_valid())

    def test_addDivision_novalues(self):
        form = ShowForm(data={'name':'', 'number':''})
        self.assertFalse(form.is_valid())

    def test_addDivision_novalues(self):
        form = ShowForm(data={'name':'hunter division', 'number':'hello'})
        self.assertFalse(form.is_valid())

#tested Showselect for

class DivisionChampTestCase(TestCase):
    def test_divisionchampform_textinintegerfields(self):
        form = DivisionChampForm(data={'champion':'henry', 'champion_pts':'8', 'champion_reserve':'jen','champion_reserve_pts':'89'})
        self.assertFalse(form.is_valid())

    def test_divisionchampform_textinintegerfields(self):
        form = DivisionChampForm(data={'champion':'212', 'champion_pts':'8', 'champion_reserve':'312','champion_reserve_pts':'89'})
        self.assertTrue(form.is_valid())

class ShowSelectFormTestCase(TestCase):
    def test_showSelectForm_invaliddatenomarks(self):
        form = ShowSelectForm(data={'date':'20191003'})
        self.assertFalse(form.is_valid())

    def test_showSelectForm_invalidorder(self):
        form = ShowSelectForm(data={'date':'10-30-3029'})
        self.assertFalse(form.is_valid())

    def test_showSelectForm_invalidstring(self):
        form = ShowSelectForm(data={'date':'30th of September'})
        self.assertFalse(form.is_valid())

    def test_showSelectForm_invalidemptyfields(self):
        form = ShowForm(data={'date':''})
        self.assertFalse(form.is_valid())

    def test_ShowSelectForm_invalid(self):
        form = ShowSelectForm(data={'date': ""})
        self.assertFalse(form.is_valid())
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


class ComboRiderTestCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()

    def test_rider_pk(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        data = {'name': "sarah", 'address': "address1", 'age': 9, 'email': "email@123.com"}
        response = self.client.post('show/horse', data)
        form = RiderForm(data)
        rider = form.save(commit=False)
        rider_pk = rider.pk
        self.assertTrue(rider_pk == "email@123.com")

class ComboHorseTestCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()

    def test_rider_pk(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        data = {"name": "Misty", "barn_name": "Misty", "age":4, "coggins":12345, "owner":"Tina", "size":"pony", "type":"shetland"}
        response = self.client.post('show/add-combo', data)
        form = HorseForm(data)
        horse = form.save(commit=False)
        horse_pk = horse.pk
        self.assertTrue(horse_pk == None)

class ComboRiderSessionTestCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()

    def test_rider_pk(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        data = {'name': "sarah", 'address': "address1", 'age': 9, 'email': "email@123.com"}
        form = RiderForm(data)
        rider = form.save(commit=False)
        session = self.client.session
        session['rider_pk'] = rider.pk
        session.save()
        self.assertTrue(session['rider_pk'] == "email@123.com")

class ComboHorseSessionTestCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()

    def test_rider_pk(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        data = {"name": "Misty", "barn_name": "Misty", "age":4, "coggins":12345, "owner":"Tina", "size":"pony", "type":"shetland"}
        form = HorseForm(data)
        horse = form.save(commit=False)
        session = self.client.session
        session['horse_pk'] = horse.pk
        session.save()
        self.assertTrue(session['horse_pk']==None)

class InvalidComboTestCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()

    def test_combo_string(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        data = {'num': "Not An Integer"}
        response = self.client.post('show/edit-combo', data)
        form = ComboNumForm(data)
        self.assertFalse(form.is_valid())

    # def test_combo_invalid_redirect(self):
    #     data = {'num': "Not An Integer"}
    #     response = self.client.post('show/edit-combo', data)
    #     form = ComboNumForm(data)
    #     self.assertTrue(c.get('index'))

class ValidComboTestCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()

    def test_combo_isvalid(self):
        data = {'num': 777}
        response = self.client.post('show/edit-combo', data)
        form = ComboNumForm(data)
        self.assertTrue(form.is_valid())


class ComboDatabaseValidTestCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()
    # def test_valid_combo_in_database(self):
    #     data_horse = {"name": "Misty", "barn_name": "Misty", "age":4, "coggins":12345, "owner":"Tina", "size":"pony", "type":"shetland"}
    #     form_horse = HorseForm(data_horse)
    #     horse = form_horse.save()
    #     data_rider = {'name': "sarah", 'address': "address1", 'age': 9, 'email': "email@123.com"}
    #     form_rider = RiderForm(data_rider)
    #     rider = form_rider.save()
    #     combo = HorseRiderCombo.objects.create(num=123, rider=rider, horse=horse)
    #     data = {'num': 777}
    #     response = self.client.post('show/edit-combo', data)
    #     combo_form = ComboNumForm(data)
    #     if combo_form.is_valid():
    #         combo_num = combo_form.cleaned_data['num']
    #     self.assertTrue(HorseRiderCombo.objects.get(num=combo_num))

class ComboDatabaseInvalidTestCase(TestCase):
    def setup(self):
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()
    def test_valid_combo_not_in_database(self):
        data_horse = {"name": "Misty", "barn_name": "Misty", "age":4, "coggins":12345, "owner":"Tina", "size":"pony", "type":"shetland"}
        form_horse = HorseForm(data_horse)
        horse = form_horse.save()
        data_rider = {'name': "sarah", 'address': "address1", 'age': 9, 'email': "email@123.com"}
        form_rider = RiderForm(data_rider)
        rider = form_rider.save()
        combo = HorseRiderCombo.objects.create(
                        num=665, rider=rider, horse=horse)

        data = {'num': 777}
        response = self.client.post('show/edit-combo', data)
        combo_form = ComboNumForm(data)
        if combo_form.is_valid():
            combo_num = combo_form.cleaned_data['num']
        try:
            HorseRiderCombo.objects.get(num=combo_num)
        except(HorseRiderCombo.DoesNotExist):
            self.assertTrue(HorseRiderCombo.DoesNotExist)
