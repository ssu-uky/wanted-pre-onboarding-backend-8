from .models import User
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError
from django.contrib.auth.hashers import make_password


# 회원가입
class SignUpSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "pk",
            "name",
            "email",
            "password",
        )

    # 비밀번호 8자 이상, 해쉬화
    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("비밀번호는 8자리 이상이어야 합니다.")
        return make_password(password)


# 로그인
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "email",
            "password",
        )
        read_only_fields = ("pk",)
