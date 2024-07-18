import json
import os

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from apiTestPlaform.settings import MEDIA_ROOT
from .models import TestFile, TestEnv, TestProject
from .serializer import TestProjectSerializer, TestFileSerializer, TestEnvSerializer
from rest_framework import permissions, mixins


class TestProjectView(ModelViewSet):
    queryset = TestProject.objects.all()
    serializer_class = TestProjectSerializer

    # 接口权限控制，传list
    permission_classes = [permissions.IsAdminUser]


class TestEnvView(ModelViewSet):
    queryset = TestEnv.objects.all()
    serializer_class = TestEnvSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["project"]


# 此处只需要继承新增、删除、查询的方法，所以只需要继承部分父类，不不继承ModelView
class TestFileView(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = TestFile.objects.all()
    serializer_class = TestFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 重写父类的新增的方法
    def create(self, request, *args, **kwargs):
        file_name = request.data['file'].name
        file_size = request.data['file'].size
        if os.path.isfile(MEDIA_ROOT / file_name):
            return Response({"msg": "文件已存在！不要重复上传！"}, status=400, )
        #
        if file_size > 1024 * 300:
            return Response({"msg": "文件不能超过1M！"}, status=400, )

        file_type = request.data["file"].content_type
        request.data["info"] = json.dumps([file_name, "Files/{}".format(file_name), file_type])
        # 此处copy调用父类方法记得把self参数去掉
        return super().create(request, *args, **kwargs)

    # 重写父类的删除方法
    def destroy(self, request, *args, **kwargs):
        # 通过get_object（）方法获得当前数据库的实例，可获得info对象
        file_path = self.get_object().info[1]
        os.remove(file_path)
        return super().destroy(request, *args, **kwargs)
