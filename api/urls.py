from django.urls import include, path

urlpatterns = [
    path('auth/', include('a_userauth.urls')),
    path('onboarding/', include('a_onboarding.urls')),
    path('profile/', include('a_profile.urls')),
    path('work/', include('a_work.urls')),
    path('bookmarks/', include('a_bookmarks.urls')),
    path('submissions/', include('a_submissions.urls')),
    path('revisions/', include('a_revisions.urls')),
]
