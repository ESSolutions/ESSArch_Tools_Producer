from rest_framework import serializers

from preingest.models import ProcessTask


class ProcessTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessTask
