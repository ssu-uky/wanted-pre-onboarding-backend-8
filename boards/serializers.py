from .models import WantedBoard
from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantedBoard
        fields = "__all__"
        
        read_only_fields = (
            "pk,",
        )
