from django.db import models
from core.apps.general.models import BaseModel




class Grade(BaseModel):
    title = models.IntegerField(
        verbose_name="Класс", unique=True,
    )
    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"
        ordering = ["pk"]

    
    def __str__(self):
        return f"{self.title}"

class Subject(BaseModel):
    title = models.CharField(
        verbose_name="Название", max_length=90,
    )
    grades = models.ManyToManyField(
        Grade, verbose_name="Классы"
    )
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ["pk"]

    
    def __str__(self):
        return self.title

class Olympiad(BaseModel):
    title = models.CharField(
        verbose_name="Название", max_length=90,
    )
    description = models.TextField(
        verbose_name="Описание олимпиады", max_length=1500,
    )
    subjects = models.ManyToManyField(
        Subject, verbose_name="Предмет"
    )
    grades = models.ManyToManyField(
        Grade, verbose_name="Классы"
    )
    tasks_in_variant = models.IntegerField(
        verbose_name="Количество заданий в варианте"
    )

    class Meta:
        verbose_name = "Олимпиада"
        verbose_name_plural = "Олимпиады"
        ordering = ["pk"]

    def __str__(self):
        return self.title


class Year(BaseModel):
    number = models.CharField(
        verbose_name="Название", max_length=90,
    )
    
    class Meta:
        verbose_name = "Год"
        verbose_name_plural = "Годы"
        ordering = ["pk"]

    
    def __str__(self):
        return self.number
    
class SolveMethod(BaseModel):
    title = models.CharField(
        verbose_name="Название", max_length=90,
    )
    
    class Meta:
        verbose_name = "Способ решения"
        verbose_name_plural = "Способ решения"
        ordering = ["pk"]

    
    def __str__(self):
        return self.title
    





class Task(BaseModel):
    title = models.CharField(
        verbose_name="Заголовок", max_length=90,
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, verbose_name="Предмет", related_name="tasks"
    )
    olympiad = models.ForeignKey(
        Olympiad, on_delete=models.PROTECT, verbose_name="Олимпиада", related_name="tasks")
    solve_method = models.ForeignKey(
        SolveMethod, on_delete=models.PROTECT, verbose_name="Метод решения", related_name="tasks")
    year = models.ForeignKey(
        Year, on_delete=models.PROTECT, verbose_name="Год", related_name="tasks")
    grade = models.ForeignKey(
        Grade, on_delete=models.PROTECT, verbose_name="Класс", related_name="tasks"
    )
    description = models.TextField(
        verbose_name="Условие задачи", max_length=1000,
    )
    tip = models.TextField(
        verbose_name="Подсказка", max_length=1000,
    )
    answer = models.CharField(
        verbose_name="Ответ", max_length=50,
    )
    solving = models.TextField(
        verbose_name="Решение", max_length=10000,
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["pk"]

    def __str__(self):
        return f"Задача № {self.title}"