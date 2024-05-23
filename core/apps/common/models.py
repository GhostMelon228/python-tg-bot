from django.db import models
from core.apps.general.models import BaseModel
from core.apps.users.models import TelegramUser
from core.apps.minor.models import Grade, Task

class ConnectionUserGrade(BaseModel):
    user = models.ForeignKey(TelegramUser, on_delete=models.PROTECT,
                             verbose_name="Пользователь", related_name="connection_user_to_grade")
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT,
                              verbose_name="Класс", related_name="connection_user_to_grade")
    class Meta:
        verbose_name = "Класс пользователя"
        verbose_name_plural = "Классы пользователя"
        ordering = ["pk"]

        unique_together = ["user", "grade"]

    def __str__(self):
        return f"Пользователь {self.user} и класс {self.grade}"

class FavouriteTasks(BaseModel):
    user = models.ForeignKey(TelegramUser, on_delete=models.PROTECT,
                             verbose_name="Пользователь", related_name="user_favourite_tasks")
    task = models.ForeignKey(Task, on_delete=models.PROTECT,
                             verbose_name="Задача", related_name="favourite_tasks")

    class Meta:
        verbose_name = "Любимая задача"
        verbose_name_plural = "Любимые задачи"
        ordering = ["pk"]

        unique_together = ["user", "task"]

    def __str__(self):
        return f"Закладка задачи №{self.pk}"
    
class UserAnswer(BaseModel):
    user = models.ForeignKey(TelegramUser, on_delete=models.PROTECT,
                             verbose_name="Пользователь", related_name="user_tries")
    task = models.ForeignKey(Task, on_delete=models.PROTECT,
                             verbose_name="Задача", related_name="user_tries")
    STATUS_CHOICES = [
        ('NA', '_'),
        ('PC', 'Решается'),
        ('WA', 'Неправильно'),
        ('OK', 'Правильно')
    ]
    status = models.CharField(
        verbose_name="Состояние задачи", max_length=15, choices=STATUS_CHOICES, default='NA', blank=True)

    class Meta:
        verbose_name = "Попытка пользователя"
        verbose_name_plural = "Попытки пользователя"
        ordering = ["pk"]

    def __str__(self):
        return f"Попытка {self.pk}"