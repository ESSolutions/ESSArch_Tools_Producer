from django.db import IntegrityError

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ip.models import (
    InformationPackage,
)

from profiles.serializers import (
    ProfileSerializer,
    ProfileLockSerializer,
    SubmissionAgreementSerializer
)

from profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileLock,
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

class ProfileLockViewSet(viewsets.ModelViewSet):
    queryset = ProfileLock.objects.all()
    serializer_class = ProfileLockSerializer

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
        information_package_id = request.data.get(
            "information_package", {}
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
            information_package = InformationPackage.objects.get(
                pk=information_package_id
            )
        except InformationPackage.DoesNotExist:
            return Response(
                {'status': 'Submission Agreement with id %s does not exist' % pk},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            profile.lock(submission_agreement, information_package)
        except IntegrityError:
            exists = ProfileLock.objects.filter(
                submission_agreement=submission_agreement,
                information_package=information_package,
                profile=profile,
            ).exists

            if exists:
                return Response(
                    {'status': 'Lock already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )


        return Response({'status': 'locking profile'})
