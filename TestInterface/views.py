from ApiTestEngine.core2.cases import run_test
from TestInterface.models import TestInterface, TestInterfaceCaseModel
from TestInterface.serializer import TestInterfaceSerializer, TestInterfaceCaseSerializer, \
    TestInterfaceCaseListSerializer, TestInterfaceCaseDetailSerializer, TestInterfaceExrendListSerializer
from Testproject.models import TestEnv
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, status
from rest_framework.response import Response

from rest_framework import mixins


# Create your views here.

class TestInterfaceView(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = TestInterface.objects.all()
    serializer_class = TestInterfaceSerializer
    # 使用登录权限类，进行接口鉴权
    permission_classes = [permissions.IsAuthenticated]
    # 增加过滤字段
    filterset_fields = ["project"]

    # 重写get_serializer_class方法，根据请求类型去获取不同的序列化器
    def get_serializer_class(self):
        if self.action == "list":
            return TestInterfaceExrendListSerializer
        else:
            return self.serializer_class

    class Meta:
        model = TestInterface
        fields = '__all__'


class TestInterfaceCaseViewSet(ModelViewSet):
    queryset = TestInterfaceCaseModel.objects.all()
    serializer_class = TestInterfaceCaseSerializer
    # 使用登录权限类，进行接口鉴权
    permission_classes = [permissions.IsAuthenticated]
    # 增加过滤字段
    filterset_fields = ["interface", "title"]

    # 重写获取列表的方法，使用新定义的TestInterfaceCaseListSerializer序列化器，只返回去用例的id和title
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TestInterfaceCaseListSerializer(queryset, many=True)
        return Response(serializer.data)

    # 重写获取详情的方法，使用新定义的序列化器TestInterfaceCaseDetailSerializer获取接口的所有序列化信息
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TestInterfaceCaseDetailSerializer(instance)
        return Response(serializer.data)

    class Meta:
        model = TestInterfaceCaseModel
        fields = '__all__'

    def run_case(self, request):
        env_id = request.data.get("env")
        cases = request.data.get("cases")
        # all函数判断可迭代对象是否都为true
        if not all([env_id, cases]):
            return Response({"error": "参数env_id和cases不能为空！"}, status=status.HTTP_400_BAD_REQUEST)
        env = TestEnv.objects.get(id=env_id)
        env_config = {
            'ENV': {
                'host': env.host,
                'headers': env.headers,
                **env.global_variable,
                **env.debug_global_variable
            },
            'DB': '',
            'global_func': env.global_func
        }
        cases_datas = [
            {
                "name": "",
                "Cases": [cases]  ##Cases传list跑多条
            }
        ]
        data= run_test(cases_datas, env_config, debug=True)

        #将data中的环境变量保存到env.debug_global_variable中
        env.debug_global_variable=data[1]
        env.save()
        return Response({"message": "ok", "result":data[0]})


'''
前端传参示例：

{
    "env": 8,
    "cases": {
        "title": "",
        "interface": {
            "url":"/api/TestInterface/interface/",
            "name":"增加测试接口",
            "method":"post"
        },
        "headers": {
        },
        "request": {
            "json": {
        "name": "调试用例运行接口",
        "method": "post",
        "url": "/run_case'",
        "type": 1,
        "project": 1
    }
        },
        "setup_script": "",
        "teardowm_script": ""
    }
}


'''
