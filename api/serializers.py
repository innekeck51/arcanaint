from rest_framework import serializers
from .models import Region, Station

class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name', 'temperature', 'humidity', 'rainfall', 'population_density', 'region_size')

class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
        fields = ('id', 'region_id', 'name', 'suhu', 'hujan', 'angin', 'sungai', 'kelembaban', 'ketinggian_sungai', 'created_at', 'updated_at')
