from rest_framework import serializers

from preingest.models import ProcessStep, ProcessTask

class PickledObjectField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data

class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep


class ProcessTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessTask

    result = PickledObjectField(allow_null=True, default=None)
