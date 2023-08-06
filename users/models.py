from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager


class User(AbstractUser):
    """ 사용자 모델 설정 "email", "password" 로 사용자 생성"""
    
    username = None
    
    name = models.CharField(
        max_length=7,
        blank=True,
        validators=[MinLengthValidator(2, "이름은 두 글자 이상이여야합니다.")],
    )
    
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        error_messages={"unique": "이미 존재하는 이메일입니다."},
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    object = CustomUserManager()
    
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "users"
        verbose_name_plural = "Users"