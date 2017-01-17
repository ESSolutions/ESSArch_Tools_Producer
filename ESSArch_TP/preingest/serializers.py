from celery import states as celery_states

from django.contrib.auth.models import User, Group, Permission

from rest_framework import serializers

from ESSArch_Core.WorkflowEngine.models import ProcessStep, ProcessTask
from ESSArch_Core.util import available_tasks

import jsonpickle
import json


class PickledObjectFieldSerializer(serializers.Field):
    def to_representation(self, obj):
        return json.loads(jsonpickle.encode(obj))

    def to_internal_value(self, data):
        return jsonpickle.decode(json.dumps(data))


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ProcessStepChildrenSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()
    id = serializers.UUIDField()
    flow_type = serializers.SerializerMethodField()
    name = serializers.CharField()
    hidden = serializers.BooleanField()
    progress = serializers.IntegerField()
    status = serializers.CharField()
    responsible = serializers.SerializerMethodField()
    step_position = serializers.SerializerMethodField()
    time_started = serializers.DateTimeField()
    time_done = serializers.DateTimeField()

    def get_url(self, obj):
        flow_type = self.get_flow_type(obj)
        request = self.context.get('request')
        url = '/api/%ss/%s/' % (flow_type, obj.pk)
        return request.build_absolute_uri(url)

    def get_flow_type(self, obj):
        return 'task' if type(obj).__name__ == 'ProcessTask' else 'step'

    def get_responsible(self, obj):
        if type(obj).__name__ == 'ProcessTask':
            if obj.responsible:
                return obj.responsible.username
            return None
        return obj.user

    def get_step_position(self, obj):
        if type(obj).__name__ == 'ProcessTask':
            return obj.processstep_pos
        return obj.parent_step_pos


class ProcessTaskSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.ChoiceField(
        choices=available_tasks(),
    )
    responsible = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = ProcessTask
        fields = (
            'url', 'id', 'name', 'status', 'progress',
            'processstep', 'processstep_pos', 'time_started',
            'time_done', 'undone', 'undo_type', 'retried',
            'responsible', 'hidden',
        )

        read_only_fields = (
            'status', 'progress', 'time_started', 'time_done', 'undone',
            'undo_type', 'retried', 'hidden',
        )


class ProcessTaskDetailSerializer(ProcessTaskSerializer):
    params = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    def get_params(self, obj):
        return dict((str(k), str(v)) for k, v in obj.params.iteritems())

    def get_result(self, obj):
        return str(obj.result)

    class Meta:
        model = ProcessTaskSerializer.Meta.model
        fields = ProcessTaskSerializer.Meta.fields + (
            'params', 'result', 'traceback', 'exception',
        )
        read_only_fields = ProcessTaskSerializer.Meta.read_only_fields + (
            'params', 'result', 'traceback', 'exception',
        )


class ProcessTaskSetSerializer(ProcessTaskSerializer):
    class Meta:
        model = ProcessTaskSerializer.Meta.model
        fields = (
            'url', 'name',
        )


class ProcessStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcessStep
        fields = (
            'url', 'id', 'name', 'result', 'type', 'user', 'parallel',
            'status', 'progress', 'undone', 'time_created', 'parent_step',
            'parent_step_pos', 'information_package',
        )
        read_only_fields = (
            'status', 'progress', 'time_created', 'time_done', 'undone',
        )


class ProcessStepDetailSerializer(ProcessStepSerializer):
    task_count = serializers.SerializerMethodField()
    failed_task_count = serializers.SerializerMethodField()
    exception = serializers.SerializerMethodField()
    traceback = serializers.SerializerMethodField()

    def get_task_count(self, obj):
        return obj.tasks.count()

    def get_failed_task_count(self, obj):
        return obj.tasks.filter(status=celery_states.FAILURE, undone=False).count()

    def get_exception(self, obj):
        t = obj.tasks.filter(status=celery_states.FAILURE, undone=False).first()
        if t:
            return t.exception

    def get_traceback(self, obj):
        t = obj.tasks.filter(status=celery_states.FAILURE, undone=False).first()
        if t:
            return t.traceback

    class Meta:
        model = ProcessStepSerializer.Meta.model
        fields = ProcessStepSerializer.Meta.fields + (
            'task_count', 'failed_task_count', 'exception', 'traceback'
        )
        read_only_fields = ProcessStepSerializer.Meta.read_only_fields + (
            'task_count', 'failed_task_count', 'exception', 'traceback'
        )


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ('url', 'id', 'name', 'codename', 'group_set')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = ('url', 'id', 'name', 'permissions',)


class GroupDetailSerializer(GroupSerializer):
    class Meta:
        model = Group
        fields = GroupSerializer.Meta.fields + (
            'user_set',
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.ReadOnlyField(source='get_all_permissions')
    user_permissions = PermissionSerializer(many=True)
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'url', 'id', 'username', 'first_name', 'last_name', 'email',
            'groups', 'is_staff', 'is_active', 'is_superuser', 'last_login',
            'date_joined', 'permissions', 'user_permissions',
        )
        read_only_fields = (
            'last_login', 'date_joined',
        )
