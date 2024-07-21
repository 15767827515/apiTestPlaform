from ApiTestEngine.core2.cases import run_test
from TestScenes.models import SceneToCase
from TestScenes.serializer import SceneToCaseListSerializer
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
        # 获取env数据，,如果没有找到返回404
        env = get_object_or_404(TestEnv, id=env_id)
        # 拼装env_config参数
        env_config = {
            'ENV': {
                'host': env.host,
                'headers': env.headers,
                **env.global_variable,

            },
            'DB': '',
            'global_func': env.global_func
        }
        # 获取task对象,如果没有找到返回404
        task = get_object_or_404(TestTaskModel, id=task_id)
        # 获取与该任务关联的所有场景
        scens_list = task.scenes.all()
        task_case_data = []
        for scene in scens_list:
            # 返回与当前 scene 相关的所有 SceneToCase 对象
            cases = scene.scenetocase_set.all()
            res = SceneToCaseListSerializer(cases, many=True).data
            sorted_res = sorted(res, key=lambda k: k['sort'])
            scene_case_list = [item["case"] for item in sorted_res]
            task_case_data.append(
                {
                    "name": scene.name,
                    "Cases": scene_case_list
                }
            )
        # 初始化创建TestRecordModel测试记录对象
        record_obj = TestRecordModel.objects.create(task=task, env=env, tester=request.user.username, status="执行中")

        result = run_test(case_data=task_case_data, env_config=env_config, debug=False)
        # 执行完任务运行后，更新TestRecordModel实例对应的属性
        record_obj.all = result["all"]
        record_obj.success = result["success"]
        record_obj.error = result["error"]
        record_obj.fail = result["fail"]
        record_obj.pass_rate = "{:.2f}".format(result["success"] / result["all"])
        record_obj.status = "执行完成"
        record_obj.save()
        # c初始化TestReport实例，保存测试报告数据到info
        report_obj = TestReport.objects.create(record=record_obj, info=result)
        report_obj.save()

        return Response(result)


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
