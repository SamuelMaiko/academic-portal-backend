from django.apps import AppConfig


class AWorkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_work'
    
    def ready(self):
        from .signals import GenerateWorkCode
