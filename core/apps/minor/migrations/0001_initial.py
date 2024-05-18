# Generated by Django 5.0.4 on 2024-05-17 20:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('title', models.IntegerField(unique=True, verbose_name='Класс')),
            ],
            options={
                'verbose_name': 'Класс',
                'verbose_name_plural': 'Классы',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='SolveMetod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=90, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Способ решения',
                'verbose_name_plural': 'Способ решения',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=90, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Год',
                'verbose_name_plural': 'Годы',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=90, verbose_name='Название')),
                ('grades', models.ManyToManyField(to='minor.grade', verbose_name='Классы')),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Olympiad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=90, verbose_name='Название')),
                ('description', models.TextField(max_length=1500, verbose_name='Описание олимпиады')),
                ('grades', models.ManyToManyField(to='minor.grade', verbose_name='Классы')),
                ('subjects', models.ManyToManyField(to='minor.subject', verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'Олимпиада',
                'verbose_name_plural': 'Олимпиады',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=90, verbose_name='Заголовок')),
                ('description', models.TextField(max_length=1000, verbose_name='Условие задачи')),
                ('tip', models.TextField(max_length=1000, verbose_name='Подсказка')),
                ('answer', models.CharField(max_length=50, verbose_name='Ответ')),
                ('solving', models.TextField(max_length=10000, verbose_name='Решение')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='minor.grade', verbose_name='Класс')),
                ('olympiad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='minor.olympiad', verbose_name='Олимпиада')),
                ('solve_metod', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='minor.solvemetod', verbose_name='Метод решения')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='minor.subject', verbose_name='Предмет')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='minor.year', verbose_name='Год')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ['pk'],
            },
        ),
    ]