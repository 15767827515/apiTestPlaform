from BugManage.models import BugHandle, BugManage
from rest_framework import serializers


class BugHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugHandle
        fields = '__all__'


class BugManageDetailSerializer(serializers.ModelSerializer):
    """bug管理的序列化器"""
    # source需要用模型中interface下面的url属性
    interface_url = serializers.StringRelatedField(source='interface.url', read_only=True)
    handle = BugHandleSerializer(many=True, source="bughandle_set", read_only=True)

    class Meta:
        model = BugManage
        fields = '__all__'


class BugManagelistSerializer(serializers.ModelSerializer):
    """bug管理的序列化器"""
    interface_url = serializers.StringRelatedField(source='interface.url', read_only=True)

    class Meta:
        model = BugManage
        fields = ['interface_url', 'create_time', 'desc', 'status', 'user', 'id']
