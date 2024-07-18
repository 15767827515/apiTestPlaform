from django.contrib import admin

# Register your models here.


from .models import TestProject,TestEnv,TestFile


@admin.register(TestProject)
class TestProjectAdmin(admin.ModelAdmin):
    list_display = ['name',"leader","created_time"]





@admin.register(TestEnv)
class TestEnvAdmin(admin.ModelAdmin):
    list_display = ['project',"global_variable",'host',"name",'global_func']




@admin.register(TestFile)
class TestFileAdmin(admin.ModelAdmin):
    list_display = ['info',"file"]