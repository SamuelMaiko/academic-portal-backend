from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="register"),
    path('get-new-otp/', views.NewOtpGenerationView.as_view(), name="get-new-otp"),
    path('login/', views.LoginView.as_view(), name="login-in"),
    path('reset-password/', views.ResetPasswordView.as_view(), name="reset-password"),
    path('reset-password-verify-otp/', views.ResetPasswordVerifyOTPView.as_view(), name="reset-password-verify-otp"),
    path('submit-new-password/', views.SubmitNewPasswordView.as_view(), name="submit-new-password"),
    path('logout/', views.LogoutView.as_view(), name="log-out"),
    path('deactivate-account/', views.DeactivateAccountView.as_view(), name="deactivate-account"),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete-account'),
    path('email-verification/', views.EmailVerificationView.as_view(), name="email-verification"),
]
