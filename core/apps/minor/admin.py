from django.contrib import admin
from core.apps.minor.models import Grade, Olympiad, SolveMetod, Subject, Task, Year


class GradeAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    list_display_links = ("pk", "title")
    search_fields = ("pk", "title")

class OlympiadAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "description")
    list_display_links = ("pk", "title", "description")
    search_fields = ("pk", "title", "description")

class SolveMetodAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    list_display_links = ("pk", "title")
    search_fields = ("pk", "title")

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    list_display_links = ("pk", "title")
    search_fields = ("pk", "title")

class TaskAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "subject", "olympiad", "solve_metod", "year", "grade", "description", "tip", "answer", "solving")
    list_display_links = ("pk", "title", "subject", "olympiad", "solve_metod", "year", "grade", "description", "tip", "answer", "solving")
    search_fields = ("pk", "title", "subject", "olympiad", "solve_metod", "year", "grade", "description", "tip", "answer", "solving")

class YearAdmin(admin.ModelAdmin):
    list_display = ("pk", "number")
    list_display_links = ("pk", "number")
    search_fields = ("pk", "number")


admin.site.register(Grade, GradeAdmin)
admin.site.register(Olympiad, OlympiadAdmin)
admin.site.register(SolveMetod, SolveMetodAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Year, YearAdmin)