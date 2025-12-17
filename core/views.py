# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
import json

from resources.models import Resource, Favorite, Rating


def home(request):
    """
    Public home page.
    - For everyone: show recent uploads + top-rated resources.
    - For logged-in users: show quick stats card (uploads, views, downloads, favorites, ratings).
    """
    stats = None

    # Recently uploaded (latest 5)
    recent_resources = Resource.objects.order_by('-created_at')[:5]

    # Top rated resources (average rating, then downloads)
    top_rated = (
        Resource.objects
        .annotate(avg_rating=Avg('ratings__stars'))
        .order_by('-avg_rating', '-download_count')
    )[:5]

    if request.user.is_authenticated:
        user = request.user

        my_resources = Resource.objects.filter(owner=user)

        uploads_count = my_resources.count()
        favorites_count = Favorite.objects.filter(user=user).count()
        ratings_received = Rating.objects.filter(resource__owner=user).count()

        total_views = my_resources.aggregate(total=Sum('view_count'))['total'] or 0
        total_downloads = my_resources.aggregate(total=Sum('download_count'))['total'] or 0

        stats = {
            "uploads_count": uploads_count,
            "favorites_count": favorites_count,
            "ratings_received": ratings_received,
            "total_views": total_views,
            "total_downloads": total_downloads,
        }

    context = {
        "stats": stats,
        "recent_resources": recent_resources,
        "top_rated": top_rated,
    }
    return render(request, "core/home.html", context)


@login_required
def dashboard(request):
    """
    Student Activity Dashboard:
    - number of uploads
    - favorites count
    - total ratings received
    - total views/downloads
    - chart data: views/downloads per your uploads
    """
    user = request.user

    my_resources = Resource.objects.filter(owner=user).order_by(
        '-view_count',
        '-download_count',
        '-created_at'
    )

    uploads_count = my_resources.count()
    favorites_count = Favorite.objects.filter(user=user).count()
    ratings_received = Rating.objects.filter(resource__owner=user).count()

    total_views = my_resources.aggregate(total=Sum('view_count'))['total'] or 0
    total_downloads = my_resources.aggregate(total=Sum('download_count'))['total'] or 0

    # Chart: each bar = one of the user's uploads
    labels = [r.title[:22] for r in my_resources]  # short titles
    views_data = [r.view_count for r in my_resources]
    downloads_data = [r.download_count for r in my_resources]

    context = {
        "user": user,
        "profile": getattr(user, "profile", None),
        "uploads_count": uploads_count,
        "favorites_count": favorites_count,
        "ratings_received": ratings_received,
        "total_views": total_views,
        "total_downloads": total_downloads,
        "labels_json": json.dumps(labels),
        "views_json": json.dumps(views_data),
        "downloads_json": json.dumps(downloads_data),
    }
    return render(request, "core/dashboard.html", context)
