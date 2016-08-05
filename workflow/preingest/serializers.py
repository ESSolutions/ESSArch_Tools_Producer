from django.contrib.auth.models import User, Group

from rest_framework import serializers

from preingest.models import ProcessStep, ProcessTask

class PickledObjectField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data

class ProcessStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcessStep
        fields = (
            'url', 'id', 'name', 'result', 'type', 'user', 'status', 'progress',
            'time_created', 'parent_step', 'archiveobject', 'tasks', 'task_set',
        )


class ProcessTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcessTask

    result = PickledObjectField(allow_null=True, default=None)
    params = serializers.JSONField()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
