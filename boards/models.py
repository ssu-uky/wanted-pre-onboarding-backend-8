from django.db import models
from common.models import CommonModel

class WantedBoard(CommonModel):
    """이력서 작성 게시판"""

    class JobTypeChoices(models.TextChoices):
        """구직자가 선택할 수 있는 직업 종류"""

        DESIGN = "DESIGN", "DESIGN"
        PM = "PM", "PM"
        FRONTEND = "FRONTEND", "FRONTEND"
        BACKEND = "BACKEND", "BACKEND"
        MARKETING = "MARKETING", "MARKETING"


    writer = models.CharField(max_length=30, blank=False, verbose_name="작성자")

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
        max_length=15,
        choices=JobTypeChoices.choices,
        blank=False,
        verbose_name="직업 종류",
    )

    links = models.URLField(blank=True, verbose_name="링크")

    def __str__(self):
        return self.writer
