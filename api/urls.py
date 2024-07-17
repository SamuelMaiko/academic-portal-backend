from django.urls import path, include

urlpatterns = [
    path('auth/', include('a_userauth.urls')),
    path('onboarding/', include('a_onboarding.urls')),
    path('profile/', include('a_profile.urls')),
    path('work/', include('a_work.urls')),
    path('bookmarks/', include('a_bookmarks.urls')),
]
