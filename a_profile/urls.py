from django.urls import path

from . import views

urlpatterns = [
    path('', views.MyProfile.as_view(), name='profile'),
    path('user/<int:id>/', views.Profile.as_view(), name='user-profile'),
    path('contact/', views.ContactInfoView.as_view(), name='contact-info'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('update/picture/', views.UpdatePictureView.as_view(), name='profile-picture'),
    path('remove-picture/', views.DeletePictureView.as_view(), name='delete-picture'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]


# Notification for uptaken and revoked work by user to the admin
# learn how the IsAdmin permission worked