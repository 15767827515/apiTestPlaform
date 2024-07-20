from django.db import models
from Testproject.models import TestProject
from TestScenes.models import Scene
from Testproject.models import TestEnv


# Create your models here.

class TestTaskModel(models.Model):
    name = models.CharField(max_length=100, help_text='任务名称', verbose_name='任务名称')
    project = models.ForeignKey(TestProject, on_delete=models.PROTECT, help_text='所属项目', verbose_name='所属项目')
    scenes = models.ManyToManyField(Scene, help_text='包含的测试业务场景', verbose_name='包含的测试业务场景')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'test_task'
        verbose_name_plural = '测试任务表'


class TestRecordModel(models.Model):
    task = models.ForeignKey(TestTaskModel, on_delete=models.PROTECT, help_text='所属测试任务',
                             verbose_name='所属测试任务')
    env = models.ForeignKey(TestEnv, on_delete=models.PROTECT, help_text='执行环境', verbose_name='执行环境')

    all = models.IntegerField(help_text='用例总数', verbose_name='用例总数', default=0, blank=True, null=True)
    success = models.IntegerField(help_text='成功用例数', verbose_name='成功用例数', default=0, blank=True, null=True)
    fail = models.IntegerField(help_text='失败用例数', verbose_name='失败用例数', default=0, blank=True, null=True)
    error = models.IntegerField(help_text='错误用例数', verbose_name='错误用例数', default=0, blank=True, null=True)
    pass_rate = models.CharField(max_length=20,help_text='用例通过率', verbose_name='用例通过率', default='0', blank=True, null=True)
    tester = models.CharField(max_length=50,help_text='执行者', verbose_name='执行者', blank=True, null=True)
    status = models.CharField(max_length=30,help_text='执行状态', verbose_name='执行状态')
    create_time = models.DateTimeField(auto_created=True, help_text='执行时间', verbose_name='执行时间')

    def __str__(self):
        return self.task.name

    class Meta:
        db_table = 'test_record'
        verbose_name_plural = '测试记录表'


class TestReport(models.Model):
    info = models.JSONField(help_text='报告数据', verbose_name='报告数据', blank=True, null=True,default=dict)
    record = models.OneToOneField(TestRecordModel, on_delete=models.PROTECT, verbose_name='测试记录',help_text='测试记录')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'test_report'
        verbose_name_plural='测试报告表'
