from django.urls import path

from . import views

urlpatterns = [
    path('', views.AccountsView.as_view(), name='accounts'),
    path('create/', views.CreateAccountView.as_view(), name='create-account'),
    path('<int:id>/', views.AccountDetailView.as_view(), name='account-detail'),
    path('<int:id>/edit/', views.EditAccountView.as_view(), name='edit-account'),
    path('<int:id>/delete/', views.DeleteAccountView.as_view(), name='delete-account'),
    path('<int:id>/deactivate/', views.DeactivateAccountView.as_view(), name='deactivate-account'),
    path('<int:id>/activate/', views.ActivateAccountView.as_view(), name='activate-account'),
    path('<int:id>/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
]
