from django.urls import path

from a_bookmarks import views as book_views
from a_profile import views as prof_views
from a_submissions import views as sub_views
from a_work import views as work_views

from . import views

urlpatterns = [
    path('', views.AccountsView.as_view(), name='accounts'),
    path('create/', views.CreateAccountView.as_view(), name='create-account'),
    path('<int:id>/', views.AccountDetailView.as_view(), name='account-detail'),
    path('<int:id>/edit/', views.EditAccountView.as_view(), name='edit-account'),
    path('<int:id>/delete/', views.DeleteAccountView.as_view(), name='delete-account'),
    path('<int:id>/deactivate/', views.DeactivateAccountView.as_view(), name='deactivate-account'),
    path('<int:id>/activate/', views.ActivateAccountView.as_view(), name='activate-account'),
    path('<int:id>/uptaken/', work_views.UserUptakenWorkView.as_view(), name='uptaken-work'),
    path('<int:id>/assigned/', work_views.UserAssignedWorkView.as_view(), name='assigned-work'),
    path('<int:id>/revoked/', work_views.UserRevokedWorkView.as_view(), name='revoked-work'),
    path('<int:id>/quality-issues-work/', work_views.UserQualityIssuesWorkView.as_view(), name='quality-issues-work'),
    path('<int:id>/analytics/', prof_views.UserAnalyticsView.as_view(), name='analytics'),
    path('general-analytics/', views.GeneralAccountAnalyticsView.as_view(), name='general-analytics'),
    path('users-performance/', views.UsersAnalyticsView.as_view(), name='users-analytics'),
    path('<int:id>/submitted-work/', sub_views.UserSubmittedWorkView.as_view(), name='submitted-work'),
    path('<int:id>/bookmarks/', book_views.UserBookmarksView.as_view(), name='bookmarks'),
    path('<int:id>/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
]
