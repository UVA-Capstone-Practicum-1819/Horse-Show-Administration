from django.db import models

# Create your models here.

class Show(models.Model):
    show_name = models.CharField(max_length=100)
    show_date = models.CharField(max_length=100)
    show_location = models.CharField(max_length=100)
    def __str__(self):
        return self.show_name

class Rider (models.Model):
    name= models.CharField(max_length= 200)
    address = models.CharField(max_length=200)
    age= models.IntegerField()
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Horse (models.Model):
    name= models.CharField(max_length= 200)
    barn_name = models.CharField(max_length=200)
    age= models.IntegerField()
    coggins= models.IntegerField()
    owner = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Classes (models.Model):
    CLASS_CHOICES = (
        ('cwu', '1. California Warm Up'),
        ('gh1', '2. Green Hunter Over Fences'),
        ('gh2', '3. Green Hunter Over Fences'),
        ('gh3', '4. Green Hunter Under Saddle'),
        ('tb1', '5. Thoroughbred Hunter Over Fences'),
        ('tb2', '6. Thoroughbred Hunter Over Fences'),
        ('tb3', '7. Thoroughbred Hunter Under Saddle'),
        ('wh1', '8. Working Hunter Over Fences'),
        ('wh2', '9. Working Hunter Over Fences'),
        ('wh3', '10. Working Hunter Under Saddle'),
        ('cae', '11. Child/Adult Equitation'),
        ('ahd1', '12. Child/Adult Hunter Over Fences'),
        ('ahd2', '13. Child/Adult Hunter Over Fences'),
        ('ahd3', '14. Child/Adult Hunter Under Saddle'),
        ('ef', '15. Child/Adult Equitation on the Flat'),
        ('hp1', '16. Horse Pleasure, Adult, Walk/Trot'),
        ('hp2', '17. Horse Pleasure, Adult, Go-As-You-Please'),
        ('hp3', '18. Horse Pleasure, Adult, Walk/Trot/Canter'),
        ('sc1', '19. Showmanship Hunter Sr.'),
        ('sc2', '20. Showmanship Hunter Jr.'),
        ('sc3', '21. Showmanship Western'),
        ('l', '22. Leadline'),
        ('sh1', '23. Pre-Short Stirrup, Walk only'),
        ('sh2', '24. Pre-Short Stirrup, Walk/Trot'),
        ('sh3', '25. Pre-Short Stirrup, Walk/Trot over Obstacles'),
        ('wp1', '26. Western Pleasure, Walk/Jog'),
        ('wp2', '27. Western Pleasure, Go-As-You-Please'),
        ('wp3', '28. Western Pleasure, Walk/Jog/Canter'),
        ('hpj1', '29. Horse Pleasure, Junior, Walk/Trot'),
        ('hpj2', '30. Horse Pleasure, Junior, Go-As-You-Please'),
        ('hpj3', '31. Horse Pleasure, Junior, Walk/Trot/Canter'),
        ('hpp1', '32. Pony Pleasure, Walk/Trot'),
        ('hpp2', '33. Pony Pleasure, Go-As-You-Please'),
        ('hpp3', '34. Pony Pleasure, Walk/Trot/Canter'),
        ('pef', '35. Pony Equitation on the Flat'),
        ('opd1', '36. 4-H Pleasure, Walk/Trot or Jog'),
        ('opd2', '37. 4-H Pleasure, Go-As-You-Please'),
        ('opd3', '38. 4-H Pleasure, Walk/Trot/Canter or lope'),
        ('ss1', '39. Short Stirrup Hunter, Walk/Trot/Canter'),
        ('ss2', '40. Short Stirrup Hunter Over Fences'),
        ('ss3', '41. Short Stirrup Hunter Over Fences'),
        ('lhd1', '42. Low Hunter Over Fences'),
        ('lhd2', '43. Low Hunter Over Fences'),
        ('lhd3', '44. Low Hunter Under Saddle'),
        ('pe2', '45. Pony Equitation for Juniors'),
        ('phd1', '46. Pony Hunter Over Fences'),
        ('phd2', '47. Pony Hunter Over Fences'),
        ('phd3', '48. Pony Hunter Under Saddle'),
    )
    type = models.BooleanField(max_length=100, choices=CLASS_CHOICES)
