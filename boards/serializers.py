from .models import WantedBoard
from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WantedBoard
        fields = (
            "id",
            "writer",
            "title",
            "contents",
            "job_type",
            "link",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("pk",)

    # job_type 입력값 대문자로 변환
    def to_internal_value(self, data):
        job_type = data.get('job_type')
        if job_type:
            data['job_type'] = job_type.upper()
        return super(BoardSerializer, self).to_internal_value(data)


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantedBoard
        fields = (
            "id",
            "writer",
            "title",
            "job_type",
        )
