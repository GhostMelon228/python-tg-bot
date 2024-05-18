from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from telegram import Update
from telegram.ext import CallbackContext

from core.apps.users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=30,
    )

    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=30,
    )

    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        unique=True,
        error_messages={"unique": "Пользователь с такой почтой уже зарегистрировался"},
    )

    #icon = models.ImageField(verbose_name="Фотография профиля", upload_to="icon/user/", blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
    )

    STATUS_CHOICES = [
        ("teacher", "Преподаватель"),
        ("student", "Студент"),
    ]
    status = models.CharField(
        verbose_name="Статус",
        max_length=7,
        choices=STATUS_CHOICES,
        default="student",
        blank=True,
    )

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь [Сайт]"
        verbose_name_plural = "1. Пользователи [Сайт]"
        ordering = ["pk"]
        db_table = "users"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class TelegramUser(models.Model):
    user_id = models.PositiveBigIntegerField()

    custom_user = models.OneToOneField(
        CustomUser,
        verbose_name="Юзер на сайте",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    username = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=256,
    )

    last_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    language_code = models.CharField(
        max_length=8,
        null=True,
        blank=True,
    )

    deep_link = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )

    is_blocked_bot = models.BooleanField(
        default=False,
    )

    is_admin = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = "Пользователь [Телеграм]"
        verbose_name_plural = "2. Пользователи [Телеграм]"
        ordering = ["pk"]
        db_table = "users_telegram"

    def __str__(self):
        return f"@{self.username}" if self.username is not None else f"{self.user_id}"

    @classmethod
    async def get_user_and_created(cls, update: Update, context: CallbackContext):
        """python-telegram-bot's Update, Context --> User instance"""
        data = extract_user_data_from_update(update)
        u, created = await cls.objects.aupdate_or_create(user_id=data["user_id"], defaults=data)

        if created:
            # Save deep_link to User model
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if (
                    str(payload).strip() != str(data["user_id"]).strip()
                ):  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created


def extract_user_data_from_update(update: Update):
    """python-telegram-bot's Update instance --> User info"""
    user = update.effective_user.to_dict()

    return dict(
        user_id=user["id"],
        is_blocked_bot=False,
        **{
            k: user[k]
            for k in ["username", "first_name", "last_name", "language_code"]
            if k in user and user[k] is not None
        },
    )