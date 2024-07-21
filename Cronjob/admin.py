from Cronjob.models import CronjobModel
from django.contrib import admin

# Register your models here.
@admin.register(CronjobModel)
class CronjobAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'task','env','name','rule','status','create_time']