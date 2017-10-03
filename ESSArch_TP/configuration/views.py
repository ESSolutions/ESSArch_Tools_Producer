from django.db.models import Q

from ESSArch_Core.configuration.models import EventType
from ESSArch_Core.configuration.views import EventTypeViewSet as CoreEventTypeViewSet


class EventTypeViewSet(CoreEventTypeViewSet):
    queryset = EventType.objects.filter(Q(eventType__range=(10100, 19999)) | Q(eventType__range=(50000, 59999)))
