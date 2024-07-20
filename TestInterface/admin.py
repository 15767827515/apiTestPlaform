from TestInterface.models import TestInterface,TestInterfaceCaseModel
from django.contrib import admin

# Register your models here.

@admin.register(TestInterface)
class TestInterfaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'method', 'url', 'type')



@admin.register(TestInterfaceCaseModel)
class TestInterfaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'interface', 'headers', 'request', 'file', 'setup_script','teardown_script')