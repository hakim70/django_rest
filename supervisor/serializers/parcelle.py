from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
from supervisor.models   import Parcelle 

class ParcelleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelle
        fields = '__all__'