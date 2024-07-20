from TestInterface.models import TestInterface, TestInterfaceCaseModel
from TestInterface.serializer import TestInterfaceSerializer, TestInterfaceCaseSerializer, \
    TestInterfaceCaseListSerializer, TestInterfaceCaseDetailSerializer,TestInterfaceExrendListSerializer
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions
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

    #重写get_serializer_class方法，根据请求类型去获取不同的序列化器
    def get_serializer_class(self):
        if self.action=="list":
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

    # 重写获取详情的方法，使用新定义的序列花器TestInterfaceCaseDetailSerializer获取接口的所有序列化信息
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TestInterfaceCaseDetailSerializer(instance)
        return Response(serializer.data)

    class Meta:
        model = TestInterfaceCaseModel
        fields = '__all__'
