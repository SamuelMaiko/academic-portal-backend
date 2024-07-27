from datetime import timedelta

from api.models import BaseModel
from django.conf import settings
from django.db import models
from django.utils import timezone


class RegistrationCode(BaseModel):
    code=models.CharField(max_length=20)
    is_used=models.BooleanField(default=False)    
    duration_to_expire = models.DurationField(default=timedelta(hours=8))
    time_to_expire = models.TimeField(null=True, blank=True)
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registration_code",
        null=True,
        blank=True
        )
    
    def __str__(self):
        return f"{None if not self.user else self.user.registration_number}'s Registration code ({self.code})"
    
    class Meta:
        db_table="registration_codes"

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.time_to_expire=(timezone.localtime(self.created_at)+self.duration_to_expire).time()
        return super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > (timezone.localtime(self.created_at)+self.duration_to_expire)