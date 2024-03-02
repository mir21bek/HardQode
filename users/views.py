from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from services.utils.send_otp import check_and_activate, send_otp_code
from users.models import CustomUser
from users.serializers import CheckOtpSerializer, RegisterSerializer


class ClientRegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "Code send successfully", 400: "Bad request"},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_otp_code(user.id)
            return Response(
                {"massage": "Code send successfully", "user email": user.email},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckOtpAPIView(APIView):
    @swagger_auto_schema(
        request_body=CheckOtpSerializer,
        responses={
            201: "User verify successfully",
            400: "Code is incorrect please check again",
        },
    )
    def post(self, request):
        serializer = CheckOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.validated_data["otp"]
            user = CustomUser.objects.filter(otp=otp, is_verify=False).first()
            if user:
                if (
                    user.otp_expiration
                    and (timezone.now() - user.otp_expiration).total_seconds() <= 180
                ):
                    return check_and_activate(user, otp)
                else:
                    return Response(
                        {"error": "Code has expired. Please request a new one."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": f"User with OTP {otp} not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
