from django.urls import path
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
]
