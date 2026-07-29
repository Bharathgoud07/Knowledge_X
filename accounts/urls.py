from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

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

    # Password reset (Django built-in views)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),

    # Resend verification link
    path(
        "resend-verification/",
        views.resend_verification,
        name="resend_verification",
    ),
]
