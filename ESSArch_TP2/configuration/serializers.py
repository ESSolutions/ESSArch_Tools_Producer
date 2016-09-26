from rest_framework import serializers

from configuration.models import (
    Agent,
    EventType,
    Parameter,
    Path,
    Schema,
)


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventType
        fields = ('url', 'id', 'eventType', 'eventDetail',)


class AgentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Agent
        fields = '__all__'

class ParameterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Parameter
        fields = '__all__'

class PathSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Path
        fields = '__all__'

class SchemaSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Schema
        fields = '__all__'
