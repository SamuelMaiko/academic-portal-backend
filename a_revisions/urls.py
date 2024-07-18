from django.urls import path

from . import views

urlpatterns = [
    path('writer-revisions/',  views.WriterRevisionsView.as_view(), name="writer-revisions"), 
    path('admin-revisions/',  views.AdminRevisionsView.as_view(), name="admin-revisions"), 
    path('<int:id>/',  views.RevisionDetailView.as_view(), name="revision-detail"), 
    path('<int:id>/delete/',  views.DeleteRevisionView.as_view(), name="delete-revision"), 
    path('<int:id>/edit/',  views.EditRevisionView.as_view(), name="edit-revision"), 
    path('<int:id>/send-message/',  views.SendRevisionMessageView.as_view(), name="send-revision-message"), 
    path('delete-message/<int:id>/',  views.DeleteRevisionMessageView.as_view(), name="delete-revision-message"), 
    path('edit-message/<int:id>/',  views.EditRevisionMessageView.as_view(), name="edit-revision-message"), 

]
