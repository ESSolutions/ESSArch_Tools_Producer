import os

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ESSArch_Core.configuration.models import (
    Path,
)

from ESSArch_Core.ip.models import (
    ArchivalInstitution,
    ArchivistOrganization,
    ArchivalLocation,
    ArchivalType,
    InformationPackage,
)

from ESSArch_Core.WorkflowEngine.models import (
    ProcessStep,
    ProcessTask,
)

from profiles.serializers import (
    ProfileSerializer,
    ProfileSASerializer,
    ProfileIPSerializer,
    SubmissionAgreementSerializer
)

from ESSArch_Core.profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileSA,
    ProfileIP,
)

from rest_framework import viewsets

class SubmissionAgreementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows submission agreements to be viewed or edited.
    """
    queryset = SubmissionAgreement.objects.all()
    serializer_class = SubmissionAgreementSerializer

    @detail_route(methods=['post'], url_path='include-type')
    def include_type(self, request, pk=None):
        sa = SubmissionAgreement.objects.get(pk=pk)
        ptype = request.data["type"]

        setattr(sa, "include_profile_%s" % ptype, True)
        sa.save()

        return Response({
            'status': 'Including profile type %s in SA %s' % (ptype, sa)
        })

    @detail_route(methods=['post'], url_path='exclude-type')
    def exclude_type(self, request, pk=None):
        sa = SubmissionAgreement.objects.get(pk=pk)
        ptype = request.data["type"]

        setattr(sa, "include_profile_%s" % ptype, False)
        sa.save()

        return Response({
            'status': 'Excluding profile type %s in SA %s' % (ptype, sa)
        })

    @detail_route(methods=["post"])
    def lock(self, request, pk=None):
        ip_id = request.data.get("ip", {})

        try:
            ip = InformationPackage.objects.get(
                pk=ip_id
            )
        except InformationPackage.DoesNotExist:
            return Response(
                {'status': 'Information Package with id %s does not exist' % ip_id},
                status=status.HTTP_404_NOT_FOUND
            )

        ip.SubmissionAgreementLocked = True
        ip.save()

        return Response({'status': 'locking submission_agreement'})

class ProfileSAViewSet(viewsets.ModelViewSet):
    queryset = ProfileSA.objects.all()
    serializer_class = ProfileSASerializer

class ProfileIPViewSet(viewsets.ModelViewSet):
    queryset = ProfileIP.objects.all()
    serializer_class = ProfileIPSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()
        profile_type = self.request.query_params.get('type', None)

        if profile_type is not None:
            queryset = queryset.filter(profile_type=profile_type)

        return queryset

    @detail_route(methods=['post'])
    def save(self, request, pk=None):
        profile = Profile.objects.get(pk=pk)
        new_data = request.data.get("specification_data", {})
        new_structure = request.data.get("structure", {})

        changed_data = (profile.specification_data.keys().sort() == new_data.keys().sort() and
                        profile.specification_data != new_data)

        changed_structure = profile.structure != new_structure

        if (changed_data or changed_structure):
            profile.copy_and_switch(
                ip=InformationPackage.objects.get(
                    pk=request.data["information_package"]
                ),
                specification_data=new_data,
                new_name=request.data["new_name"],
                structure=new_structure,
            )
            return Response({'status': 'saving profile'})

        return Response({'status': 'no changes, not saving'}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=["post"])
    def lock(self, request, pk=None):
        profile = self.get_object()

        ip_id = request.data.get(
            "information_package", {}
        )

        try:
            ip = InformationPackage.objects.get(
                pk=ip_id
            )
        except InformationPackage.DoesNotExist:
            return Response(
                {'status': 'Information Package with id %s does not exist' % ip_id},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            ProfileIP.objects.get(profile=profile, ip=ip).lock(request.user)
        except ProfileIP.DoesNotExist:
            ProfileIP.objects.create(profile=profile, ip=ip).lock(request.user)

        if profile.profile_type == "sip":
            root = os.path.join(
                Path.objects.get(
                    entity="path_preingest_prepare"
                ).value,
                str(ip.pk)
            )

            step = ProcessStep.objects.create(
                name="Create Physical Model",
                information_package=ip
            )
            task = ProcessTask.objects.create(
                name="preingest.tasks.CreatePhysicalModel",
                params={
                    "structure": profile.structure,
                    "root": root
                },
                information_package=ip
            )

            step.tasks = [task]
            step.save()
            step.run()
        elif profile.profile_type == "transfer_project":
            data = profile.specification_data

            archival_institution = data.get("archival_institution")
            archivist_organization = data.get("archivist_organization")
            archival_type = data.get("archival_type")
            archival_location = data.get("archival_location")

            if archival_institution:
                (arch, _) = ArchivalInstitution.objects.get_or_create(
                    name = archival_institution
                )
                ip.ArchivalInstitution = arch

            if archivist_organization:
                (arch, _) = ArchivistOrganization.objects.get_or_create(
                    name = archivist_organization
                )
                ip.ArchivistOrganization = arch

            if archival_type:
                (arch, _) = ArchivalType.objects.get_or_create(
                    name = archival_type
                )
                ip.ArchivalType = arch

            if archival_location:
                (arch, _) = ArchivalLocation.objects.get_or_create(
                    name = archival_location
                )
                ip.ArchivalLocation = arch

            ip.save()

        return Response({'status': 'locking profile'})
