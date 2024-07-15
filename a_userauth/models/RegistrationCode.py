from api.models import BaseModel
from django.db import models
from django.conf import settings
    
class RegistrationCode(BaseModel):
    code=models.CharField(max_length=6)
    is_used=models.BooleanField(default=True)    
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="registration_code", null=True)
    
    def __str__(self):
        return f"{self.user.registration_number}'s Registration code ({self.code})"
    
    class Meta:
        db_table="registration_codes"