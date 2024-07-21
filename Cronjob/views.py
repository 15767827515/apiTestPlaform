import json

from Cronjob.models import CronjobModel
from Cronjob.serializer import CronjobSerializer
from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.viewsets import GenericViewSet
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.db import transaction
from rest_framework.response import Response


# Create your views here.


class CronjobViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = CronjobModel.objects.all()
    serializer_class = CronjobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['project', "task"]

    # 重写创建定时任务的接口
    def create(self, request, *args, **kwargs):
        """创建定时任务的方法"""
        # 开启视图
        with transaction.atomic():
            # 创建一个事物保存节点
            save_point = transaction.savepoint()
            try:
                # 调用父类的方法创建一条定时任务（只是在CronJob表中新赠一条数据）
                result = super().create(request, *args, **kwargs)
                # 获取创建定时任务的规则
                rule = result.data.get('rule').split(" ")
                rule_dict = dict(zip(['minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year'], rule))
                # 使用django-celer-beat中的CrontabSchedule模型创建一个规则对象
                try:
                    cron = CrontabSchedule.objects.get(**rule_dict)
                except:
                    cron = CrontabSchedule.objects.create(**rule_dict)
                # 使用django-celer-beat中的PeriodicTask创建一个周期性调度任务
                PeriodicTask.objects.create(
                    name=result.data.get('id'),
                    task='TestTasks.celery_tasks.run_taskcase_celry',
                    crontab=cron,
                    kwargs=json.dumps({
                        "env_id": result.data.get('env'),
                        "task_id": result.data.get('task'),
                        "tester": request.user.username
                    }),
                    enabled=result.data.get('status'),
                )
            except:
                # 进行事物回滚
                transaction.savepoint_rollback(save_point)
                return Response({'error': "定时任务创建失败！"}, status=500)
            else:
                # 提交事物
                transaction.savepoint_commit(save_point)
                return Response(result.data)
