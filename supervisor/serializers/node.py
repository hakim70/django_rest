from rest_framework import serializers
from supervisor.models import Node

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'