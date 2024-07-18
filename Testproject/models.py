from django.db import models


# Create your models here.


class TestProject(models.Model):
    name = models.CharField(max_length=50, help_text='项目名字', verbose_name="项目名字")
    leader = models.CharField(max_length=20, help_text='测试人名字', verbose_name="测试人名字")
    created_time = models.DateTimeField(auto_now=True, help_text='创建时间', verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table='Testproject'
        verbose_name_plural='测试项目表'


class TestFile(models.Model):
    file = models.FileField(help_text='测试文件', verbose_name="测试文件")
    info = models.JSONField(help_text='测试文件数据信息', verbose_name="测试文件数据信息",default=list)

    def __str__(self):
        return str(self.info)

    class Meta:
        db_table = 'TestFile'
        verbose_name_plural = '测试文件表'



class TestEnv(models.Model):
    project = models.ForeignKey(TestProject,on_delete=models.CASCADE,help_text='项目关联外键', verbose_name="项目关联外键")
    global_variable = models.JSONField(help_text='全局变量', verbose_name="全局变量",default=dict,null=True,blank=True)
    debug_global_variable = models.JSONField(help_text='debug模式全局变量', verbose_name="debug模式全局变量",default=dict,null=True,blank=True)
    db = models.JSONField(help_text='数据库配置', verbose_name="数据库配置",default=dict,null=True)
    host = models.CharField(max_length=200,help_text='全局域名配置', verbose_name="全局域名配置",null=True,blank=True)
    headers = models.JSONField(help_text='全局请求头', verbose_name="全局请求头",default=dict,null=True,blank=True)
    global_func = models.TextField(help_text='全局自定义函数', verbose_name="全局自定义函数",null=True,blank=True)
    name = models.CharField(max_length=50,help_text='测试环境名字', verbose_name="测试环境名字",default=list)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'TestEnv'
        verbose_name_plural = '测试环境表'
