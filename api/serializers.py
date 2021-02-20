from rest_framework import serializers
from .models import Region

class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name', 'temperature', 'humidity', 'rainfall', 'population_density', 'region_size')
