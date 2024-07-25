from django.apps import AppConfig


class AUserauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_userauth'
    
    def ready(self):
        from .signals import (
            CreateUserProfile,
            EmailAccountCredentials,
            GenerateRegistrationNumber,
            SendOTP,
            SendVerificationOTP,
            SendWelcomeEmail,
        )
    
