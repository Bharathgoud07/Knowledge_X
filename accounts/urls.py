# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    # Profile (self)
    path("profile/", views.my_profile, name="my_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("change-password/", views.change_password, name="change_password"),

    # Public profile (view others)
    path("u/<int:user_id>/", views.public_profile, name="public_profile"),

    # Email verification
    path(
        "verify-email/<uidb64>/<token>/",
        views.verify_email,
        name="verify_email",
    ),

    # Optional OTP login
    path(
        "login/otp/",
        views.login_with_email_request,
        name="login_with_email_request",
    ),
    path(
        "login/otp/verify/",
        views.login_with_email_verify,
        name="login_with_email_verify",
    ),

    # ✅ Resend verification link
    path(
        "resend-verification/",
        views.resend_verification,
        name="resend_verification",
    ),
]
