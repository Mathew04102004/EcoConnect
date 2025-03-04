from rest_framework import serializers
from .models import WastePickup

class WastePickupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastePickup
        fields = '__all__'
