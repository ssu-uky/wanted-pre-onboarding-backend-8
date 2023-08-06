from django.db import models
from common.models import CommonModel


class WantedBoard(CommonModel):
    """이력서 작성 게시판"""

    class JobTypeChoices(models.TextChoices):
        """구직자가 선택할 수 있는 직종"""

        DESIGN = "디자인"
        PM = "기획"
        FRONTEND = "프론트엔드"
        BACKEND = "백엔드"
        MARKETING = "마케팅"
        ETC = "기타"

    title = models.CharField(
        max_length=30,
        blank=False,
        verbose_name="제목",
    )

    content = models.TextField(
        max_length=300,
        blank=False,
        verbose_name="내용",
    )

    job_type = models.CharField(
        max_length=20,
        blank=False,
    )

    Links = models.URLField()

    file = models.URLField()
