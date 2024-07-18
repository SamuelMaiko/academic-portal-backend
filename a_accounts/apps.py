from django.apps import AppConfig


class AAccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_accounts'
    
    def ready(self):
        from .signals import (
            AccountActivationEmail,
            AccountDeactivationEmail,
            AccountDeletionEmail,
            PasswordResetEmail,
        )