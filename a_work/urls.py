from django.urls import path

from a_revisions import views as rev_views
from a_submissions import views as sub_views

from . import views

urlpatterns = [
    path('',  views.WorkView.as_view(), name="work"),
    path('<int:id>/',  views.WorkDetailView.as_view(), name="work-detail"),
    path('create/',  views.CreateWorkView.as_view(), name="create-work"),
    path('<int:id>/edit/',  views.EditWorkView.as_view(), name="edit-work"),
    path('<int:id>/delete/',  views.DeleteWorkView.as_view(), name="delete-work"),
    path('<int:id>/uptake/',  views.UptakeWorkView.as_view(), name="uptake-work"),
    path('<int:id>/revoke/',  views.RevokeWorkView.as_view(), name="revoke-work"),
    path('<int:id>/assign/',  views.AssignWorkView.as_view(), name="assign-work"),
    path('uptaken/',  views.UptakenWorkView.as_view(), name="uptaken-work"),
    path('assigned/',  views.AssignedWorkView.as_view(), name="assigned-work"),
    path('<int:id>/read/',  views.MarkAsReadView.as_view(), name="mark-work-as-read"),
    path('<int:id>/submit/',  sub_views.SubmitWorkView.as_view(), name="submit-work"),
    path('<int:id>/submissions/',  sub_views.WorkSubmissionsView.as_view(), name="work-submissions"),
    path('<int:id>/revisions/',  rev_views.WorkRevisionsView.as_view(), name="work-revisions"),
    path('<int:id>/create-revision/',  rev_views.CreateRevisionView.as_view(), name="create-revision"),
]
