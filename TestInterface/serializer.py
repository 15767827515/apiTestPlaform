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
    interface=TestInterfaceSerializer()
    class Meta:
        model = TestInterfaceCaseModel
        fields = "__all__"


# 重新定义的给测试用例详情方法的序列化器，返回带有TestInterfaceSerializer序列化字段的信息
class TestInterfaceCaseDetailSerializer(serializers.ModelSerializer):
    interface = TestInterfaceSerializer(read_only=True)

    class Meta:
        model = TestInterfaceCaseModel
        fields = "__all__"


#定义给测试接口列表获取关联用例的序列化器，以便接口列表可以返回关联的case字段
class TestInterfaceExrendListSerializer(serializers.ModelSerializer):
    #使用测试用例的Te，stInterfaceCaseListSerializer序列化器返回id和title，source传入测试用例模型TestInterfaceCaseModel集
    cases = TestInterfaceCaseListSerializer()

    class Meta:
        model = TestInterface
        fields = '__all__'
