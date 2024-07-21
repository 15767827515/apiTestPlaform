import Cronjob
from Cronjob.models import CronjobModel
from rest_framework import serializers


class CronjobSerializer(serializers.ModelSerializer):
    project_name = serializers.StringRelatedField(read_only=True, source='project.name')
    task_name= serializers.StringRelatedField(read_only=True, source='task.name')

    class Meta:
        model = CronjobModel
        fields = '__all__'
