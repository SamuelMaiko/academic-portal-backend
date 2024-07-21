from django.urls import path

from . import views

urlpatterns = [
    path('',  views.SubmissionsView.as_view(), name="submissions"),
    path('all/',  views.AllSubmissionsView.as_view(), name="all-submissions"),
    path('<int:id>/',  views.SubmissionsDetailView.as_view(), name="submissions-details"),
    path('<int:id>/claim/',  views.ClaimSubmissionView.as_view(), name="claim-submission"),
    path('<int:id>/delete/',  views.DeleteSubmissionsView.as_view(), name="delete-submission"),
    path('<int:id>/edit/',  views.EditSubmissionsView.as_view(), name="edit-submission"),
]
