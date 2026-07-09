from rest_framework import serializers
from .models import TankLevel

class TankLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TankLevel
        fields = ['level_percentage', 'source', 'recorded_at']
        read_only_fields = ['recorded_at']