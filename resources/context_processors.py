# resources/context_processors.py
from .models import Notification


def notifications_count(request):
    """
    Adds unread notification count AND latest unread notifications
    to every template context for the navbar dropdown.
    """
    if request.user.is_authenticated:
        unread_qs = Notification.objects.filter(user=request.user, is_read=False)
        count = unread_qs.count()
        # Latest 5 for navbar dropdown preview
        header = unread_qs.order_by("-created_at")[:5]
    else:
        count = 0
        header = []

    return {
        "notifications_unread_count": count,
        "notifications_header": header,
    }
