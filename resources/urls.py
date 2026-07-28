from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    # List + CRUD-ish
    path("", views.resource_list, name="resource_list"),
    path("upload/", views.upload_resource, name="upload_resource"),
    path("<int:pk>/", views.resource_detail, name="resource_detail"),
    path("<int:pk>/download/", views.resource_download, name="resource_download"),

    # Online viewer & AI Chat
    path("<int:pk>/view/", views.resource_viewer, name="resource_viewer"),
    path("<int:pk>/chat/", views.resource_chat_api, name="resource_chat_api"),

    # Favorites
    path("<int:pk>/favorite/", views.toggle_favorite, name="resource_toggle_favorite"),
    path("favorites/", views.my_favorites, name="my_favorites"),

    # Dashboards / analytics
    path("subject-dashboard/", views.subject_dashboard, name="subject_dashboard"),
    path("admin-analytics/", views.admin_analytics_dashboard, name="admin_analytics"),
    path("admin/users/", views.admin_user_list, name="admin_user_list"),
    path("admin/users/<int:user_id>/", views.admin_user_detail, name="admin_user_detail"),
    path("admin/resources/", views.admin_resource_list, name="admin_resource_list"),
    path("admin/resources/<int:pk>/edit/", views.admin_resource_edit, name="admin_resource_edit"),
    path("admin/reports/", views.admin_report_list, name="admin_report_list"),
    path("admin/subjects/", views.admin_subject_list, name="admin_subject_list"),
    path("admin/subjects/add/", views.admin_subject_add, name="admin_subject_add"),
    path("admin/subjects/<int:pk>/edit/", views.admin_subject_edit, name="admin_subject_edit"),
    path("admin/subjects/<int:pk>/delete/", views.admin_subject_delete, name="admin_subject_delete"),
    path("admin/notifications/send/", views.admin_send_notification, name="admin_send_notification"),
    path("my-activity/", views.my_activity, name="my_activity"),

    # Reports + verification
    path("<int:pk>/report/", views.report_resource, name="report_resource"),
    path("<int:pk>/verify/", views.verify_resource, name="verify_resource"),

    # Delete resource
    path("<int:pk>/delete/", views.delete_resource, name="resource_delete"),

    # Notifications
    path("notifications/", views.notifications_list, name="notifications_list"),
    path("notifications/<int:pk>/read/", views.notification_mark_read, name="notification_mark_read"),
    path("notifications/mark-all-read/", views.mark_all_notifications_read, name="mark_all_notifications_read"),

    # Leaderboard
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
