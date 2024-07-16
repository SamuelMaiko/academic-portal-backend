from django.urls import path
from . import views

urlpatterns = [
    path('details/',  views.Details.as_view(), name="get-details"),
]
