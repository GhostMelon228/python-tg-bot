from django.contrib import admin
from core.apps.common.models import ConnectionUserGrade, FavouriteTasks, UserTry, UsedUserTip, UserTaskEnroll

class ConnectionUserGradeAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "grade")
    list_display_links = ("pk", "user", "grade")
    search_fields = ("pk", "user", "grade")

class FavouriteTasksAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "task")
    list_display_links = ("pk", "user", "task")
    search_fields = ("pk", "user", "task")

class UserTriesAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "task", "status")
    list_display_links = ("pk", "user", "task", "status")
    search_fields = ("pk", "user", "task", "status")

class UserTaskEnrollAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "task", "status")
    list_display_links = ("pk", "user", "task", "status")
    search_fields = ("pk", "user", "task", "status")

class UsedUserTipAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "task")
    list_display_links = ("pk", "user", "task")
    search_fields = ("pk", "user", "task")

admin.site.register(ConnectionUserGrade, ConnectionUserGradeAdmin)
admin.site.register(FavouriteTasks, FavouriteTasksAdmin)
admin.site.register(UserTry, UserTriesAdmin)
admin.site.register(UserTaskEnroll, UserTaskEnrollAdmin)
admin.site.register(UsedUserTip, UsedUserTipAdmin)