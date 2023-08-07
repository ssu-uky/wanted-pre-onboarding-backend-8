from .models import WantedBoard
from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantedBoard
        fields = (
            "id",
            "writer",
            "title",
            "content",
            "job_type",
            "links",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("pk",)
