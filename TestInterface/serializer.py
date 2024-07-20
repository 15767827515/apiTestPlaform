from rest_framework import serializers, viewsets
from TestInterface.models import TestInterface, TestInterfaceCaseModel


class TestInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestInterface
        fields = '__all__'


class TestInterfaceCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestInterfaceCaseModel
        fields = '__all__'


class TestInterfaceCaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestInterfaceCaseModel
        fields = ["id", "title"]


#重新定义的给测试用例详情方法的序列化器，返回带有TestInterfaceSerializer序列化字段的信息
class TestInterfaceCaseDetailSerializer(serializers.ModelSerializer):
    interface=TestInterfaceSerializer(read_only=True)
    class Meta:
        model = TestInterfaceCaseModel
        fields = "__all__"
