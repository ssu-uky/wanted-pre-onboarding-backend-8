from django.contrib import admin
from . import models


@admin.register(models.WantedBoard)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "job_type",
        "writer",
        "links",
    )

    list_display_links = ("writer", "title", "job_type")
    list_filter = ("job_type",)
