from django.urls import path
from .views import (
    RegisterView,
    VerifyEmail,
    LoginAPIView,
    RequestPasswordResetEmailView,
    PasswordTokenCheckAPIView,
    SetNewPasswordAPIView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path(
        "reset-password/",
        RequestPasswordResetEmailView.as_view(),
        name="reset-password",
    ),
    path(
        "reset-password-confirm/<uidb64>/<token>/",
        PasswordTokenCheckAPIView.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "reset-password-complete",
        SetNewPasswordAPIView.as_view(),
        name="reset-password-complete",
    ),
]
