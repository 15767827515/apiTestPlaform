from django.contrib import admin
from BugManage.models import BugManage, BugHandle


# Register your models here.

@admin.register(BugManage)
class BugManageAdmin(admin.ModelAdmin):
    list_display = ('interface', 'create_time', 'desc', 'info', 'status', 'user')


@admin.register(BugHandle)
class BugHandleAdmin(admin.ModelAdmin):
    list_display = ('bug', 'create_time', 'update_user', 'handle_status')
