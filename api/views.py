from django.shortcuts import render

from django.shortcuts import render
from rest_framework import viewsets

from .serializers import RegionSerializer
from .models import Region

from rest_framework.decorators import action
from rest_framework.response import Response
from api.lib.promethee import Promethee

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all().order_by('name')
    serializer_class = RegionSerializer

    @action(methods=['post'], detail=False)
    def calculate(self, request):
        pref  = 'usual'
        param = {'p': 1, 'q': 1, 'sigma': 0}
        
        input_data      = request.data['input_data']
        input_weight    = request.data['input_weight']
        input_threshold = request.data['input_threshold']

        process = Promethee(data_sendiri = input_data, data_threshold = input_threshold, data_weight = input_weight)
        process.startPromethee(preference_function=pref, function_params=param)

        last_index = len(process.phi_global)

        ranked = sorted(process.phi_global, reverse=False)
        for idx, val in enumerate(ranked):
            if process.phi_global[last_index-1] == val:
                output_rank = idx+1
            
        output_total = process.phi_global
        output_netflow = process.phi_global[last_index-1]

        return Response({"output_total": output_total, "output_netflow": output_netflow, "output_rank": output_rank})