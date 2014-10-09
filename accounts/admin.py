from django.contrib import admin
import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(models.Profile, ProfileAdmin)
