from django.test import TestCase
from show.models import Show, Rider, Horse, Classes, Combo
from show import models

# Create your tests here.


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
    def create_rider(self, title="test", body="test for rider"):
        return Rider.objects.create(name = "Lauren", address="234 cotton lane", age=12, email="sdd3ee@virginia.edu")

    def test_rider_creation(self):
        testrider = self.create_rider()
        self.assertTrue(isinstance(testrider, Rider))

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

class HorseTestCase(TestCase):
    def create_horse(self, title="test", body="test for horse"):
        return Horse.objects.create(name = "Smokey Mountain", barn_name="Smokey", age=10, coggins=10102, owner="Tina", size="pony", type="shetland")

    def test_horse_creation(self):
        testhorse = self.create_horse()
        self.assertTrue(isinstance(testhorse, Horse))

class ComboTestCase(TestCase):
    def create_combo(self, title="test", body="test for add combo"):
        return Combo.objects.create(combo='234', ridername="Richard Lee", horsename = "Jenny", owner="John Doe")

    def test_create_combo(self):
        test_combo = self.create_combo()
        self.assertTrue(isinstance(test_combo, Combo))

class ComboIntTestCase(TestCase):
    def create_combo(self, title="test", body="test for add int combo"):
        return Combo.objects.create(combo=564, ridername="Jane Doe", horsename = "Toby", owner="Oliver Parker")

    def test_create_combo(self):
        test_combo = self.create_combo()
        self.assertTrue(isinstance(test_combo, Combo))

class ComboRandomTestCase(TestCase):
    def create_combo(self, title="test", body="test for add random combo"):
        return Combo.objects.create(combo= models.random_string(), ridername="Jane Doe", horsename = "Toby", owner="Oliver Parker")

    def test_create_combo(self):
        test_combo = self.create_combo()
        self.assertTrue(isinstance(test_combo, Combo))

class RandomCombinationTestCase1(TestCase):
    def generate_random_three_digit_int(self, title="test", body="test for three digit integer"):
        return models.random_string()
    def test_generate_random(self):
        for i in range (10):
            test_random_int = self.generate_random_three_digit_int()
            self.assertTrue(len(test_random_int), 3)

class RandomCombinationTestCase2(TestCase):
    def generate_random_int(self, title="test", body="test for integer range"):
        return models.random_string()
    def test_generate_random(self):
        for i in range (10):
            test_random_int = self.generate_random_int()
            self.assertTrue(0 <= int(test_random_int) <= 999)