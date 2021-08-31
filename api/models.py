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

class Station(models.Model):
    id = models.AutoField(primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, null=False)
    suhu = models.IntegerField()
    hujan = models.IntegerField()
    angin = models.IntegerField()
    sungai = models.IntegerField(default=0)
    kelembaban = models.IntegerField(default=0)
    ketinggian_sungai = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,  blank=True)

    def __str__(self):
        return self.name
