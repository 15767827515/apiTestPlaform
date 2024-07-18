from rest_framework import serializers

from Testproject.models import TestProject, TestEnv, TestFile


class TestProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestProject
        fields = '__all__'


class TestEnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestEnv
        fields = '__all__'


class TestFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestFile
        fields = '__all__'
