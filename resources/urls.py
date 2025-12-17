# resources/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # List + CRUD-ish
    path("", views.resource_list, name="resource_list"),
    path("upload/", views.upload_resource, name="upload_resource"),
    path("<int:pk>/", views.resource_detail, name="resource_detail"),
    path("<int:pk>/download/", views.resource_download, name="resource_download"),

    # Online viewer
    path("<int:pk>/view/", views.resource_viewer, name="resource_viewer"),

    # Favorites
    path("<int:pk>/favorite/", views.toggle_favorite, name="resource_toggle_favorite"),
    path("favorites/", views.my_favorites, name="my_favorites"),

    # Dashboards / analytics
    path("subject-dashboard/", views.subject_dashboard, name="subject_dashboard"),
    path("admin-analytics/", views.admin_analytics_dashboard, name="admin_analytics"),
    path("my-activity/", views.my_activity, name="my_activity"),

    # Reports + verification
    path("<int:pk>/report/", views.report_resource, name="report_resource"),
    path("<int:pk>/verify/", views.verify_resource, name="verify_resource"),

    # Notifications
    path("notifications/", views.notifications_list, name="notifications_list"),
    path("notifications/<int:pk>/read/", views.notification_mark_read, name="notification_mark_read"),

    # Leaderboard
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
