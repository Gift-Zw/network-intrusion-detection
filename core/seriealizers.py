# serializers.py
from rest_framework import serializers
from .models import NetworkTraffic


class NetworkTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkTraffic
        fields = '__all__'
