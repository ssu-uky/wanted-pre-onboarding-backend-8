from django.contrib import admin
from . import models


@admin.register(models.WantedBoard)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "contents",
        "job_type",
        "writer",
        "link",
    )

    list_display_link = ("writer", "title", "job_type")
    list_filter = ("job_type",)
    readonly_fields = ("created_at", "updated_at")
