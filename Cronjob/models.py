from django.db import models
from Testproject.models import TestProject, TestEnv
from TestTasks.models import TestTaskModel


# Create your models here.


class CronjobModel(models.Model):
    project = models.ForeignKey(TestProject, on_delete=models.CASCADE, help_text='所属项目', verbose_name='所属项目')
    task = models.ForeignKey(TestTaskModel, on_delete=models.CASCADE, help_text='所属测试任务',
                             verbose_name='所属测试任务')
    env = models.ForeignKey(TestEnv, on_delete=models.CASCADE, help_text='测试的环境',
                            verbose_name='测试的环境')
    name = models.CharField(max_length=30, help_text='定时任务的名字', verbose_name='定时任务的名字')
    rule = models.CharField(max_length=100, help_text='定时任务的规则', verbose_name='定时任务的规则')
    status = models.BooleanField(help_text='定时任务状态', verbose_name='定时任务状态', default=False)
    create_time = models.BooleanField(help_text='定时任务创建时间', verbose_name='定时任务创建时间', auto_created=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Cronjob'
        verbose_name_plural = '定时任务表'
