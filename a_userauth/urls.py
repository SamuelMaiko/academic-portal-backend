from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name="registration"),
    path('email-verification/', views.EmailVerificationView.as_view(), name="email-verification"),
    path('get-new-otp/', views.NewOtpGenerationView.as_view(), name="new-otp"),
    path('login/', views.LoginView.as_view(), name="login-in"),
    path('logout/', views.LogoutView.as_view(), name="log-out"),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name="forgot-password"),
    path('verify-otp/', views.VerifyOTPView.as_view(), name="verify-otp"),
    path('reset-password/', views.ResetPasswordView.as_view(), name="reset-password"),
]
