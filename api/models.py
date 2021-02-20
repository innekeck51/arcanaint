from django.db import models

class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, null=False)
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    rainfall = models.IntegerField()
    population_density = models.IntegerField()
    region_size = models.IntegerField()

    def __str__(self):
        return self.name 
