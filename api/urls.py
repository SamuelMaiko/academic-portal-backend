from django.urls import include, path

from . import views

urlpatterns = [
    path('auth/', include('a_userauth.urls')),
    path('onboarding/', include('a_onboarding.urls')),
    path('profile/', include('a_profile.urls')),
    path('work/', include('a_work.urls')),
    path('bookmarks/', include('a_bookmarks.urls')),
    path('submissions/', include('a_submissions.urls')),
    path('revisions/', include('a_revisions.urls')),
    path('accounts/', include('a_accounts.urls')),
    path('notifications/', include('a_notifications.urls')),
    path('preferences/', include('a_preferences.urls')),
    path('first/', views.FirstUserRegistrationNumber.as_view()),
]
