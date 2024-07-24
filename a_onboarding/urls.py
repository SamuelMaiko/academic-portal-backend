from django.urls import path

from . import views

urlpatterns = [
    path('details/',  views.Details.as_view(), name="get-details"),
    path('fill-details/',  views.FillDetails.as_view(), name="fill-details"),
    path('complete-profile/',  views.CompleteProfileView.as_view(), name="complete-profile"),
]
