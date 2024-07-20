from django.db import models
from Testproject.models import TestProject


# Create your models here.


class TestInterface(models.Model):
    CHOICES = {
        (1, "项目接口"),
        (2, "第三方接口")
    }
    project = models.ForeignKey(TestProject, on_delete=models.CASCADE, help_text='所属项目', verbose_name='所属项目')
    name = models.CharField(max_length=100, help_text='接口名字', verbose_name='接口名字')
    method = models.CharField(max_length=50, help_text='请求方式', verbose_name='请求方式')
    url = models.CharField(max_length=100, help_text='请求url', verbose_name='请求url')
    type = models.IntegerField(choices=CHOICES, help_text='接类类型', verbose_name='接口类型', default=1)

    def __str__(self):
        return self.url

    class Meta:
        db_table = 'interface'
        verbose_name_plural = '接口表'


class TestInterfaceCaseModel(models.Model):
    title = models.CharField(max_length=100, help_text="用例名称", verbose_name='用例名称')
    interface = models.ForeignKey(TestInterface, on_delete=models.CASCADE, help_text="所属接口",
                                  verbose_name='所属接口')
    headers = models.JSONField(help_text="请求头配置", verbose_name='请求头配置', default=dict, blank=True, null=True)
    request = models.JSONField(help_text="请求参数配置", verbose_name='请求参数配置', default=dict, blank=True,
                               null=True)
    file = models.JSONField(help_text="请求上传文件的参数", verbose_name='请求上传文件的参数', default=list, blank=True,
                            null=True)
    setup_script = models.TextField(help_text="前置脚本", verbose_name='前置脚本', default='', blank=True, null=True)
    teardown_script = models.TextField(help_text="后置脚本", verbose_name='后置脚本', default='', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'interface_case'
        verbose_name_plural = '测试用例表'
