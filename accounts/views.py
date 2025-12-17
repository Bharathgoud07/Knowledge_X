# accounts/views.py
from datetime import timedelta, date
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Count, Sum, F
from django.db.models.functions import Coalesce

from .models import Profile, LoginOTP
from .forms import (
    RegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    EmailLoginForm,
    OTPLoginRequestForm,
    OTPVerifyForm,
)

from resources.models import Resource


# ----------------------------------------------------
# Helper: send verification email
# ----------------------------------------------------
def send_verification_email(request, user):
    """
    Create (if needed) Profile and send a verification email
    with a uid + token link.
    """
    Profile.objects.get_or_create(user=user)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verify_url = request.build_absolute_uri(
        reverse("verify_email", kwargs={"uidb64": uid, "token": token})
    )

    subject = "Verify your email for Knowledgex"
    message = (
        f"Hi {user.username},\n\n"
        f"Please verify your email by clicking this link:\n{verify_url}\n\n"
        f"If you did not register, you can ignore this email."
    )

    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
        [user.email],
        fail_silently=True,  # will just log in console backend
    )


# ----------------------------------------------------
# Email verification handler
# ----------------------------------------------------
def verify_email(request, uidb64, token):
    """
    When user clicks the email link, mark profile.email_verified = True.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        profile, _ = Profile.objects.get_or_create(user=user)
        if not profile.email_verified:
            profile.email_verified = True
            profile.email_verified_at = timezone.now()
            profile.save()
        messages.success(request, "Email verified successfully. You can now log in.")
    else:
        messages.error(request, "Invalid or expired verification link.")

    return redirect("login")


# ----------------------------------------------------
# REGISTER
# ----------------------------------------------------
def register_user(request):
    """
    Register with:
    - username
    - email
    - password + confirm_password

    Username and email both unique.
    Sends a verification email (optional to enforce later).
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            # Ensure profile exists
            Profile.objects.get_or_create(user=user)

            # Send verification mail (in dev, you see it in console)
            try:
                send_verification_email(request, user)
            except Exception:
                # Don't break registration if mail backend fails
                pass

            messages.success(
                request,
                "Account created successfully! Please check your email for a verification link. You can still log in now.",
            )
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


# ----------------------------------------------------
# LOGIN (email OR username + password)
# ----------------------------------------------------
def login_user(request):
    """
    Login using either:
    - email + password  OR
    - username + password

    The form field is a single "identifier" (email or username).
    """
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"].strip()
            password = form.cleaned_data["password"]

            user_obj = None

            # Try email first if it looks like an email
            if "@" in identifier:
                user_obj = User.objects.filter(email__iexact=identifier).first()

            # If not found by email, try username
            if user_obj is None:
                user_obj = User.objects.filter(username__iexact=identifier).first()

            if user_obj is None:
                messages.error(request, "Invalid email/username or password.")
            else:
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password,
                )
                if user is None:
                    messages.error(request, "Invalid email/username or password.")
                else:
                    # Optional: login streak update
                    profile, _ = Profile.objects.get_or_create(user=user)
                    today = date.today()
                    last = profile.last_login_date

                    if last is None:
                        profile.login_streak = 1
                    else:
                        if last == today:
                            # same-day login – keep streak
                            pass
                        elif last == today - timedelta(days=1):
                            profile.login_streak += 1
                        else:
                            profile.login_streak = 1

                    if profile.login_streak > profile.longest_streak:
                        profile.longest_streak = profile.login_streak

                    profile.last_login_date = today
                    profile.save()

                    login(request, user)
                    messages.success(request, "Logged in successfully.")
                    return redirect("home")
    else:
        form = EmailLoginForm()

    return render(request, "accounts/login.html", {"form": form})


# ----------------------------------------------------
# LOGOUT
# ----------------------------------------------------
def logout_user(request):
    logout(request)
    return redirect("login")


# ----------------------------------------------------
# VIEW OWN PROFILE
# ----------------------------------------------------
@login_required
def my_profile(request):
    profile = request.user.profile

    fields_to_check = {
        "Bio": profile.bio,
        "College": profile.college,
        "Branch": profile.branch,
        "GitHub": profile.github,
        "LinkedIn": profile.linkedin,
        "Profile picture": profile.picture,
    }

    filled = sum(1 for v in fields_to_check.values() if v)
    total = len(fields_to_check) or 1
    profile_completion = int((filled / total) * 100)
    missing_fields = [key for key, val in fields_to_check.items() if not val]

    context = {
        "profile": profile,
        "profile_completion": profile_completion,
        "missing_fields": missing_fields,
    }
    return render(request, "accounts/profile.html", context)


# ----------------------------------------------------
# EDIT OWN PROFILE
# ----------------------------------------------------
@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("my_profile")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "u_form": u_form,
            "p_form": p_form,
            "profile": profile,
        },
    )


# ----------------------------------------------------
# CHANGE PASSWORD
# ----------------------------------------------------
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("my_profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {"form": form})


# ----------------------------------------------------
# PUBLIC PROFILE (view other users)
# ----------------------------------------------------
@login_required
def public_profile(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    profile = target_user.profile

    uploads_qs = Resource.objects.filter(owner=target_user)
    uploads_count = uploads_qs.count()
    favorites_count = target_user.favorites.count()
    comments_count = target_user.comments.count()
    total_downloads = uploads_qs.aggregate(total=Sum("download_count"))["total"] or 0

    # Score
    score = uploads_count * 3 + total_downloads + comments_count

    # Rank by score
    ranking_qs = (
        User.objects.annotate(
            u_count=Count("resources"),
            d_total=Sum("resources__download_count"),
            c_count=Count("comments"),
        )
        .annotate(
            score=(
                F("u_count") * 3
                + Coalesce(F("d_total"), 0)
                + F("c_count")
            )
        )
        .order_by("-score")
    )

    rank = 1
    for idx, u in enumerate(ranking_qs, start=1):
        if u.id == target_user.id:
            rank = idx
            break

    # Badges
    badges = []
    if uploads_count >= 1:
        badges.append("New Uploader")
    if uploads_count >= 10:
        badges.append("Active Contributor")
    if total_downloads >= 50:
        badges.append("Popular Resources")
    if comments_count >= 20:
        badges.append("Community Helper")

    # Activity chart – last 6 uploads
    last_uploads = uploads_qs.order_by("-created_at")[:6][::-1]
    chart_labels = [r.created_at.strftime("%d %b") for r in last_uploads]
    chart_downloads = [r.download_count for r in last_uploads]

    context = {
        "profile_user": target_user,
        "profile": profile,
        "uploads_count": uploads_count,
        "favorites_count": favorites_count,
        "comments_count": comments_count,
        "total_downloads": total_downloads,
        "rank": rank,
        "badges": badges,
        "chart_labels_json": json.dumps(chart_labels),
        "chart_downloads_json": json.dumps(chart_downloads),
    }
    return render(request, "accounts/public_profile.html", context)


# ----------------------------------------------------
# OPTIONAL: EMAIL + OTP LOGIN (kept for future use)
# ----------------------------------------------------
def login_with_email_request(request):
    """
    Step 1: user enters email, we send them a 6-digit OTP.
    """
    if request.method == "POST":
        form = OTPLoginRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            user = User.objects.filter(email__iexact=email).first()

            if not user:
                messages.error(request, "No account found with that email.")
                return redirect("login_with_email_request")

            profile, _ = Profile.objects.get_or_create(user=user)
            if not profile.email_verified:
                messages.error(request, "Email is not verified. Please verify via registration email.")
                return redirect("login")

            import random
            code = f"{random.randint(100000, 999999)}"
            LoginOTP.objects.create(user=user, code=code)

            subject = "Your KnowledgeX login OTP"
            message = (
                f"Hi {user.username},\n\n"
                f"Your OTP for login is: {code}\n\n"
                f"It is valid for 10 minutes.\n"
            )
            send_mail(
                subject,
                message,
                getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
                [user.email],
                fail_silently=True,
            )

            messages.success(request, "OTP sent to your email. Enter it below.")
            return redirect(f"{reverse('login_with_email_verify')}?email={email}")
    else:
        form = OTPLoginRequestForm()

    return render(request, "accounts/login_otp_request.html", {"form": form})


def login_with_email_verify(request):
    """
    Step 2: user enters email + OTP, we log them in if correct.
    """
    initial_email = request.GET.get("email", "")
    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            code = form.cleaned_data["code"].strip()

            user = User.objects.filter(email__iexact=email).first()
            if not user:
                messages.error(request, "Invalid email or OTP.")
                return redirect("login_with_email_verify")

            otp_obj = (
                LoginOTP.objects.filter(user=user, code=code, is_used=False)
                .order_by("-created_at")
                .first()
            )

            if not otp_obj or not otp_obj.is_valid():
                messages.error(request, "Invalid or expired OTP.")
                return redirect("login_with_email_verify")

            otp_obj.is_used = True
            otp_obj.save()

            login(request, user)
            messages.success(request, "Logged in successfully with OTP!")
            return redirect("home")
    else:
        form = OTPVerifyForm(initial={"email": initial_email})

    return render(request, "accounts/login_otp_verify.html", {"form": form})


# ----------------------------------------------------
# RESEND VERIFICATION EMAIL
# ----------------------------------------------------
@login_required
def resend_verification(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.email_verified:
        messages.info(request, "Your email is already verified.")
    else:
        send_verification_email(request, request.user)
        messages.success(request, "Verification email sent again.")
    return redirect("my_profile")
