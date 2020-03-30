from django.db import models

# Create your models here.
class Country(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=251)
    flag = models.CharField(max_length=251)
    reports=models.CharField(max_length=251)
    cases=models.CharField(max_length=251)
    deaths=models.CharField(max_length=251)
    recovered=models.CharField(max_length=251)
    lat=models.CharField(max_length=251)
    lng=models.CharField(max_length=251)
    deltaCases=models.CharField(max_length=251)
    deltaDeaths = models.CharField(max_length=251)

    def __str__(self):
        return self.name