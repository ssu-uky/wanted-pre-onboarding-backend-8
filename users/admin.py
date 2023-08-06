from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "User Profile",
            {
                "fields": (
                    "email",
                    "password",
                    "is_admin",
                ),
                "classes": ("wide", "extrapretty"),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_staff", "is_superuser", "user_permissions"),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("pk", "email", "is_admin")
    list_display_links = ("pk", "email")

    # pk 최근 가입 순으로 정렬
    ordering = ("-pk",)
