# resources/context_processors.py
from .models import Notification

def notifications_count(request):
    """
    Adds unread notification count to every template.
    """
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        count = 0
    return {"unread_notifications_count": count}
