from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.apps.users.models import CustomUser, TelegramUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "status",
    )
    list_display_links = (
        "id",
        "first_name",
        "last_name",
        "email",
    )
    search_fields = (
        "id",
        "first_name",
        "last_name",
        "email",
    )
    list_filter = (
        "first_name",
        "last_name",
    )
    fieldsets = (
        (
            "Основная информация",
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "icon",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "status",
                ),
            },
        ),
        (
            "Пароль",
            {
                "classes": ("wide",),
                "fields": ("password",),
            },
        ),
    )
    add_fieldsets = (
        (
            "Создать пользователя",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ("id",)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "custom_user",
    )
    list_display_links = (
        "id",
        "user_id",
        "custom_user",
    )