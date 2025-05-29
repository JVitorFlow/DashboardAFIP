from rest_framework import serializers
from .models import ShiftData


class ShiftDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftData
        fields = '__all__'
        read_only_fields = ('id',)    


class ShiftDataMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftData
        fields = ["recipiente"]