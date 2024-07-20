from BugManage import models
from TestInterface.serializer import TestInterfaceCaseListSerializer
from TestScenes.models import Scene, SceneToCase
from rest_framework import serializers

TestInterfaceCaseListSerializer


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = '__all__'


class SceneToCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneToCase
        fields = '__all__'


class SceneToCaseListSerializer(serializers.ModelSerializer):
    case = TestInterfaceCaseListSerializer()
    scenes = SceneSerializer()

    class Meta:
        model = SceneToCase
        fields = '__all__'
        read_only_fields = ('id',)
