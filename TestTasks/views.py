from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, mixins
from TestTasks.models import TestTaskModel, TestRecordModel, TestReport
from TestTasks.serializer import TestTaskSerializer, TestTaskDetailSerializer, TestRecordSerializer, \
    TestReportSerializer
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
    queryset = TestRecordModel.objects.all()
    serializer_class = TestRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 指定使用自定义的过滤器类
    filterset_class = TestRecordFilter


class TestReportView(mixins.ListModelMixin,
                     GenericViewSet):
    queryset = TestReport.objects.all()
    serializer_class = TestReportSerializer
    permission_classes = [permissions.IsAuthenticated]
