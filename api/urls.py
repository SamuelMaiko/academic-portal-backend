from django.urls import path, include

urlpatterns = [
    path('auth/', include('a_userauth.urls')),
    path('profile/', include('a_profile.urls')),
]
