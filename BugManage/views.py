from django.db import transaction
from django.shortcuts import render
from BugManage.models import BugHandle, BugManage
from BugManage.serializer import BugManageDetailSerializer, BugHandleSerializer,BugManagelistSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from BugManage.models import BugHandle, BugManage
from rest_framework import status


# Create your views here.


class BugManageViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = BugManage.objects.all()
    serializer_class = BugManagelistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return BugManagelistSerializer
        else:
            return BugManageDetailSerializer

    # 重写新增bug的接口
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            savepoint = transaction.savepoint()
            # 调用父类的create方法创建BugManage对象
            try:
                result = super().create(request, *args, **kwargs)
                # 根据创建的对象BugManage的id获取具体的BugManage对象
                bug_manage = BugManage.objects.get(id=result.data.get("id"))
                handle_status = f"提交BUG，BUG的处理状态是{result.data.get('status')}"
                # 在关联的BugHandle表中新增对应的记录
                bug_handle = BugHandle.objects.create(bug=bug_manage,
                                                      update_user=request.user.username,
                                                      handle_status=handle_status
                                                      )
            except:
                return Response({"error": "新增bug失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERRORT)
            else:
                return result
