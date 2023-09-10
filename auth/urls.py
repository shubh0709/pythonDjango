from django.urls import path

from .views import create_user, send_otp, verify_otp

urlpatterns = [
    path("sendOTP", view=send_otp),
    path("verifyOTP", view=verify_otp),
    path("createUser", view=create_user),
]
