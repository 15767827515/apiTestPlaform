from TestScenes.models import Scene,SceneToCase
from django.contrib import admin

# Register your models here.

@admin.register(Scene)
class ScenesAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name')



@admin.register(SceneToCase)
class SceneToCaseAdmin(admin.ModelAdmin):
    list_display =("id","scenes","case","sort")