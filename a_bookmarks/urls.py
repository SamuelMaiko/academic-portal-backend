from django.urls import path
from . import views

urlpatterns = [
    path('',  views.BookmarksView.as_view(), name="bookmarks"),
    path('add/<int:work_id>/',  views.AddBookmarkView.as_view(), name="add-bookmark"),
    path('remove/<int:work_id>/',  views.RemoveBookmarkView.as_view(), name="remove-bookmark"),
]
