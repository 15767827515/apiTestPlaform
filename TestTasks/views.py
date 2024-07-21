from ApiTestEngine.core2.cases import run_test
from TestScenes.models import SceneToCase
from TestScenes.serializer import SceneToCaseListSerializer
from TestTasks.celery_tasks import  run_taskcase_celry
from Testproject.models import TestEnv
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, generics, mixins, status
from TestTasks.models import TestTaskModel, TestRecordModel, TestReport
from TestTasks.serializer import TestTaskSerializer, TestTaskDetailSerializer, TestRecordSerializer, \
    TestReportSerializer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


# Create your views here.

class TestTaskViewSet(viewsets.ModelViewSet):
    queryset = TestTaskModel.objects.all()
    serializer_class = TestTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['project']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestTaskDetailSerializer
        else:
            return self.serializer_class

    def run_task(self, request):
        # 从请求参数中获取env_id和scenes_id
        env_id = request.data['env_id']
        task_id = request.data['task_id']
        if not env_id:
            return Response({'error': 'env_id is empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not task_id:
            return Response({'error': 'task_id is empty'}, status=status.HTTP_400_BAD_REQUEST)
        tester=request.user.username
        #异步调用run_taskcase_celry方法
        run_taskcase_celry.delay(env_id, task_id, tester)
        return Response({"message": "测试计划成功运行，请等待运行结果！"}, status=status.HTTP_200_OK)


from django_filters import rest_framework as filters


class TestRecordFilter(filters.FilterSet):
    # 定义自定义过滤器，因为project在模型中没有直接定义，所以借助关联关联字段task实例中的project属性获得project
    project = filters.NumberFilter(field_name='task__project')

    class Meta:
        model = TestRecordModel
        fields = ['project', "task"]


class TestRecordView(
    mixins.ListModelMixin,
    GenericViewSet):
    # 对查询出来的查询集按create_time降序排序
    queryset = TestRecordModel.objects.all().order_by('-create_time')
    serializer_class = TestRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 指定使用自定义的过滤器类
    filterset_class = TestRecordFilter


# 定义TestReportView的过滤器类
class TestReportFilter(filters.FilterSet):
    # 根据rocord实例下的id进行顾虑，语法record__id
    record_id = filters.NumberFilter(field_name='record__id')

    class Meta:
        model = TestReport
        fields = ['record_id']


class TestReportView(mixins.ListModelMixin,
                     GenericViewSet):
    queryset = TestReport.objects.all()
    serializer_class = TestReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TestReportFilter
