from rest_framework import serializers
from supervisor.models   import Localisation

class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = '__all__'