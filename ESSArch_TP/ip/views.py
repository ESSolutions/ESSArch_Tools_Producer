from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ip.models import (
    ArchivalInstitution,
    ArchivistOrganization,
    ArchivalType,
    ArchivalLocation,
    InformationPackage,
    EventIP
)

from preingest.models import (
    ProcessStep,
    ProcessTask,
)

from ip.serializers import (
    ArchivalInstitutionSerializer,
    ArchivistOrganizationSerializer,
    ArchivalTypeSerializer,
    ArchivalLocationSerializer,
    InformationPackageSerializer,
    InformationPackageDetailSerializer,
    EventIPSerializer,
)

from rest_framework import viewsets

class ArchivalInstitutionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archival institutions to be viewed or edited.
    """
    queryset = ArchivalInstitution.objects.all()
    serializer_class = ArchivalInstitutionSerializer

class ArchivistOrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archivist organizations to be viewed or edited.
    """
    queryset = ArchivistOrganization.objects.all()
    serializer_class = ArchivistOrganizationSerializer

class ArchivalTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archival types to be viewed or edited.
    """
    queryset = ArchivalType.objects.all()
    serializer_class = ArchivalTypeSerializer

class ArchivalLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archival locations to be viewed or edited.
    """
    queryset = ArchivalLocation.objects.all()
    serializer_class = ArchivalLocationSerializer

class InformationPackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows information packages to be viewed or edited.
    """
    queryset = InformationPackage.objects.all()
    serializer_class = InformationPackageSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return InformationPackageSerializer

        return InformationPackageDetailSerializer

    def create(self, request):
        """
        Prepares a new information package (IP) using the following tasks:

        1. Creates a new IP in the database.

        2. Creates a directory in the prepare directory with the name set to
        the id of the new IP.

        3. Creates an event in the database connected to the IP and with the
        detail "Prepare IP".

        Args:

        Returns:
            None
        """

        label = request.data.get('label', None)
        responsible = self.request.user.username or "Anonymous user"

        step = ProcessStep.objects.create(
            name="Prepare IP",
        )

        t1 = ProcessTask.objects.create(
            name="preingest.tasks.PrepareIP",
            params={
                "label": label,
                "responsible": responsible,
                "step": str(step.pk),
            },
            processstep_pos=0,
        )

        t2 = ProcessTask.objects.create(
            name="preingest.tasks.CreateIPRootDir",
            params={
            },
            result_params={
                "information_package": t1.pk
            },
            processstep_pos=1,
        )

        t3 = ProcessTask.objects.create(
            name="preingest.tasks.CreateEvent",
            params={
                "detail": "Prepare IP",
            },
            result_params={
                "information_package": t1.pk
            },
            processstep_pos=2,
        )

        step.tasks = [t1, t2, t3]
        step.save()
        step.run()

        return Response({"status": "Prepared IP"})

    @detail_route(methods=['post'], url_path='create')
    def create_ip(self, request, pk=None):
        """
        Creates the specified information package

        Args:
            pk: The primary key (id) of the information package to prepare

        Returns:
            None
        """
        try:
            InformationPackage.objects.get(pk=pk).create()
            return Response({'status': 'creating ip'})
        except InformationPackage.DoesNotExist:
            return Response(
                {'status': 'Information package with id %s does not exist' % pk},
                status=status.HTTP_404_NOT_FOUND
            )


class EventIPViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = EventIP.objects.all()
    serializer_class = EventIPSerializer
