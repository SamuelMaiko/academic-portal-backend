from django.urls import path

from . import views

urlpatterns = [
    path('', views.NotificationsView.as_view(), name='notifications'),
    path('<int:id>/delete/', views.DeleteNotificationView.as_view(), name='delete-notification'),
    path('read-all-notifications/', views.ReadAllNotificationsView.as_view(), name='read-all-notifications'),
    path('unread-notifications-count/', views.UnreadNotificationsCountView.as_view(), name='unread-notifications-count'),
]
