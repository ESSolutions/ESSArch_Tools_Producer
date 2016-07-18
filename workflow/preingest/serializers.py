from rest_framework import serializers

from preingest.models import ProcessStep, ProcessTask


class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep


class ProcessTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessTask
