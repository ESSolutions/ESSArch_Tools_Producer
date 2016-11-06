from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ESSArch_Core.ip.models import (
    InformationPackage,
)

from profiles.serializers import (
    ProfileSerializer,
    ProfileSALockSerializer,
    SAIPLockSerializer,
    SubmissionAgreementSerializer
)

from ESSArch_Core.profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileSALock,
    SAIPLock,
)

from rest_framework import viewsets

class SubmissionAgreementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows submission agreements to be viewed or edited.
    """
    queryset = SubmissionAgreement.objects.all()
    serializer_class = SubmissionAgreementSerializer

    @detail_route(methods=['put'], url_path='change-profile')
    def change_profile(self, request, pk=None):
        sa = SubmissionAgreement.objects.get(pk=pk)
        new_profile = Profile.objects.get(pk=request.data["new_profile"])

        sa.change_profile(new_profile=new_profile)

        return Response({
            'status': 'updating SA (%s) with new profile (%s)' % (
                sa, new_profile
            )
        })


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
        sa = get_object_or_404(SubmissionAgreement, pk=pk)

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

        try:
            sa.lock(ip)
        except IntegrityError:
            exists = SAIPLock.objects.filter(
                submission_agreement=sa, information_package=ip,
            ).exists

            if exists:
                return Response(
                    {'status': 'Lock already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )


        return Response({'status': 'locking submission_agreement'})

class ProfileSALockViewSet(viewsets.ModelViewSet):
    queryset = ProfileSALock.objects.all()
    serializer_class = ProfileSALockSerializer

class SAIPLockViewSet(viewsets.ModelViewSet):
    queryset = SAIPLock.objects.all()
    serializer_class = SAIPLockSerializer

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
                submission_agreement=SubmissionAgreement.objects.get(
                    pk=request.data["submission_agreement"]
                ),
                specification_data=new_data,
                new_name=request.data["new_name"],
                structure=new_structure,
            )
            return Response({'status': 'saving profile'})

        return Response({'status': 'no changes, not saving'}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=["post"])
    def lock(self, request, pk=None):
        profile = Profile.objects.get(pk=pk)

        submission_agreement_id = request.data.get(
            "submission_agreement", {}
        )

        try:
            submission_agreement = SubmissionAgreement.objects.get(
                pk=submission_agreement_id
            )
        except SubmissionAgreement.DoesNotExist:
            return Response(
                {'status': 'Submission Agreement with id %s does not exist' % pk},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            profile.lock(submission_agreement)
        except IntegrityError:
            exists = ProfileSALock.objects.filter(
                submission_agreement=submission_agreement, profile=profile,
            ).exists

            if exists:
                return Response(
                    {'status': 'Lock already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )


        return Response({'status': 'locking profile'})
