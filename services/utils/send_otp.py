import random
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from config import email

from users.models import CustomUser


def generate_code_for_send_mail(length=4):
    otp = "".join(random.choice("0123456789") for _ in range(length))
    return otp


def check_and_activate(user, otp):
    if user:
        if not user.is_verify:
            user.is_verify = True
            user.otp = None
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_201_CREATED,
            )
    else:
        return Response(
            {"message": "User is already verified."},
            status=status.HTTP_400_BAD_REQUEST,
        )


def send_otp_code(user_id):
    user = CustomUser.objects.get(id=user_id)
    subject = f"Mail confirmation {user_id}"
    otp = generate_code_for_send_mail()
    user.otp = otp
    user.otp_expiration = timezone.now()
    user.save()
    message = (
        f"Dear {user.user_name}\n\nyou have successfully registered,"
        f" please confirm your e-mail. Enter the 4-digit code below\n\n{otp}"
    )
    to_email = user.email
    from_email = email.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email], fail_silently=False)
    return user
