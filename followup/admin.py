from django.contrib import admin

import models


class TaskAdmin(admin.ModelAdmin):
    list_display = ('client', 'author', 'content', 'due_date', 'is_done')
    date_hierarchy = 'due_date'
    list_filter = ('client',)

    def get_queryset(self, request):
        tasks = models.Task.objects.pending_for_user(request.user)
        return tasks.order_by('-due_date')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(models.Task, TaskAdmin)
