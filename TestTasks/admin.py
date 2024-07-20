from TestTasks.models import TestTaskModel,TestRecordModel,TestReport
from django.contrib import admin

# Register your models here.

@admin.register(TestTaskModel)
class TestTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' , 'project')


@admin.register(TestRecordModel)
class TestRecordModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'task' , 'env','all','success','fail','error','pass_rate','tester','status','create_time')



@admin.register(TestReport)
class TestTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'info' , 'info')