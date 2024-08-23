from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
from supervisor.models   import Project 


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'