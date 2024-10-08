from rest_framework import serializers
from .models import ShiftData


class ShiftDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftData
        fields = '__all__'
