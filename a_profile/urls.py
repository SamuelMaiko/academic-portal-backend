from django.urls import path
from . import views

urlpatterns = [
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]


# setting up tabnine
# test endpoints monitor ONBOARDING
# learn change pass logic 
# create and update methods in serilaizers with SOURCE
# consider query on the CHANGE PASSWORD
# on login send the details: profile_completed, password_changed
# commit and push 
