from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.ClientRegisterAPIView.as_view(), name="client_register"),
    path("otp_checker/", views.CheckOtpAPIView.as_view(), name="otp_checker"),
]
