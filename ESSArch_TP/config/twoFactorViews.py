import django_otp
from ESSArch_Core.auth.serializers import LoginSerializer
from django_otp import devices_for_user, user_has_device
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.response import Response
from rest_framework import serializers, views, permissions, status
from rest_auth.views import (
    LoginView as rest_auth_LoginView,
)

from django_otp import _user_is_anonymous

from django.contrib.auth import get_user_model
User = get_user_model()


class TwoFactorUserSerializer(serializers.ModelSerializer):

    def get_url(self, obj):
        return "otp_dummy_url"

    def get_permissions(self, obj):
        return obj.get_all_permissions()

    def update(self, instance, validated_data):
        print("in UserLoggedInSerializer.update")

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = (
            'url', 'id', 'username', 'first_name', 'last_name', 'email',
            'is_staff', 'is_active', 'is_superuser', 'last_login',
            'date_joined', 'user_permissions',
        )
        read_only_fields = (
            'id', 'username', 'last_login', 'date_joined', 'organizations',
            'is_staff', 'is_active', 'is_superuser',
        )


class OTPLogin(rest_auth_LoginView):
    serializer_class = LoginSerializer

    def process_login(self):
        print(f"#### in process_login.....")
        user = self.request.user

        if _user_is_anonymous(user):
            print("  User is annonymous")
        elif user.is_authenticated():
            device = get_user_totp_device(user=user, confirmed=True)
            print("  User is authenticated")
            if device:
                print(f"  User got device: '{device}', TODO: WE SHOULD HANDLE OTP here!!!")
            else:
                print(f"  User got no device...")
        else:
            print(f"  in else in get_response...")

        super().process_login()

    def get_response(self):
        print("#### in OPTLogin.get_response")
        print(f"  token: '{self.token}'")
        user = self.request.user

        if _user_is_anonymous(user):
            print("  User is annonymous")
        elif user.is_authenticated():
            device = get_user_totp_device(user=user, confirmed=True)
            print("  User is authenticated")
            if device:
                print(f"  User got device: '{device}', doing otp_login!!!")
                django_otp.login(self.request, device)
            else:
                print(f"  User got no device...")
        else:
            print(f"  in else in get_response...")

        serializer = TwoFactorUserSerializer(instance=self.user, context={'request': self.request})

        return Response(serializer.data)


# Backwards compatibility.
login = OTPLogin.as_view()


def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


class TOTPVerifyView(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        token = request.data.get('token')
        device = get_user_totp_device(user)
        if device is not None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class IsOtpVerified(permissions.BasePermission):
    """
    If user has verified TOTP device, require TOTP OTP.
    """
    message = "You do not have permission to perform this action until you verify your OTP device."

    def otp_is_verified(self, request):
        user = request.user
        return hasattr(user, 'otp_device') and user.is_verified()

    def has_permission(self, request, view):
        if user_has_device(request.user):
            return self.otp_is_verified(request)
        else:
            return True


class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)


class TOTPDeleteView(views.APIView):
    """
    Use this endpoint to delete a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated, IsOtpVerified]

    def post(self, request, format=None):
        user = request.user
        devices = devices_for_user(user)
        for device in devices:
            device.delete()
        user.save()
        return Response(status=status.HTTP_200_OK)


# TODO: delete this class, this is only for ease the deletion of TOTP under development
class TOTPFreeDeleteView(views.APIView):
    """
    Use this endpoint to delete a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        devices = devices_for_user(user)
        for device in devices:
            device.delete()
        user.save()
        return Response(status=status.HTTP_200_OK)
