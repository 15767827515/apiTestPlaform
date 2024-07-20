from TestTasks.models import TestTaskModel, TestRecordModel, TestReport
from rest_framework import serializers
from TestScenes.serializer import SceneSerializer


class TestTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTaskModel
        fields = '__all__'


class TestTaskDetailSerializer(serializers.ModelSerializer):
    scenes = SceneSerializer(many=True)

    class Meta:
        model = TestTaskModel
        fields = '__all__'


class TestRecordSerializer(serializers.ModelSerializer):
    #task会返回TestTaskModel实例对象的__str__的值,也就是定义的self.name值
    task = serializers.StringRelatedField(read_only=True)
    #env会返回实TestEnv例对象的__str__的值，也就是定义的self。name值
    env=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TestRecordModel
        fields = '__all__'


class TestReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestReport
        fields = '__all__'
