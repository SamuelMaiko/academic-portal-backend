from django.db import models
from django.conf import settings
from api.models import BaseModel 

class Onboarding(BaseModel):
    details_filled=models.BooleanField(default=False)
    profile_completed=models.BooleanField(default=False)
    is_changed_password=models.BooleanField(default=False)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')

    class Meta:
        db_table = "onboarding"  

    def __str__(self):
        return f'Onboarding for user {self.user.registration_number}'
        