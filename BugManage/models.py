from django.db import models
from TestInterface.models import TestInterface


# Create your models here.


class BugManage(models.Model):
    interface = models.ForeignKey(TestInterface, on_delete=models.CASCADE, help_text='所属接口',
                                  verbose_name='所属接口')
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')
    desc = models.TextField(max_length='200', help_text='bug描述信息', verbose_name='bug描述信息', null=True, blank=True)
    info = models.JSONField(help_text='bug的用例详情', verbose_name='bug的用例详情', null=True, blank=True,
                            default=dict)
    status = models.CharField(max_length=20, help_text='bug状态', verbose_name='bug状态')
    user = models.CharField(max_length=30, help_text='提交人', verbose_name='提交人', null=True, blank=True)

    class Meta:
        db_table = "bug"
        verbose_name_plural = 'bug管理表'


class BugHandle(models.Model):
    bug = models.ForeignKey(BugManage, on_delete=models.CASCADE, help_text='bug', verbose_name='bug')
    create_time = models.DateTimeField(auto_now_add=True, help_text='提交时间', verbose_name='提交时间')
    update_user = models.CharField(max_length=30, help_text='提交人', verbose_name='提交人', null=True, blank=True)
    handle_status = models.CharField(max_length=30, help_text='bug的处理操作', verbose_name='bug的处理操作', null=True,
                                     blank=True)

    class Meta:
        db_table = "bugHandle"
        verbose_name_plural = 'bug操作记录'
