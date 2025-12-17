# resources/middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import Visit

class VisitMiddleware(MiddlewareMixin):
    """
    Simple middleware that saves each page visit (except static/admin).
    """

    def process_response(self, request, response):
        try:
            path = request.path or ""
            # Ignore static, media, admin, favicon
            if (
                path.startswith("/static/")
                or path.startswith("/media/")
                or path.startswith("/admin/")
                or path == "/favicon.ico"
            ):
                return response

            # Only log "normal" pages (GET requests are enough)
            if request.method not in ("GET", "POST"):
                return response

            Visit.objects.create(
                user=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
                path=path,
                method=request.method,
                is_authenticated=bool(getattr(request, "user", None) and request.user.is_authenticated),
            )
        except Exception:
            # Never break the site because of analytics
            pass

        return response
