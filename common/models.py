from django.db import models


# Create your models here.
class CommonModel(models.Model):
    
    """공통적으로 사용 될 모델 / 생성시간, 수정시간"""
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
