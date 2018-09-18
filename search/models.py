from django.db import models

# Create your models here.

from django.db import models

class House(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    area = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return 'name = ' + self.name + '\ncity =' + self.city + '\nlocation = ' + self.location + '\narea = ' + str(self.area) + '\nprice = ' + str(self.price) + '\n'
