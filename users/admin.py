from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "User Profile",
            {
                "fields": (
                    "name",
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
    
    list_display = ("pk", "name", "email", "is_admin")
    list_display_links = ("pk", "name", "email")
    
    # pk 내림차순으로 정렬
    ordering = ("-pk",)