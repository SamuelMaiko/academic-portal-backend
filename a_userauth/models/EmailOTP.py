from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
import uuid

class EmailOTP(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="email_otp")
    otp=models.CharField(max_length=6)
    temp_token=models.UUIDField(default=uuid.uuid4, editable=False)
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s OTP"
    
    class Meta:
        db_table="OTP"
    
    @property
    def is_expired(self):
        expiration_time=timedelta(minutes=5)
        # print((timezone.now()-self.timestamp))
        return (timezone.now()-self.timestamp)>expiration_time
    
    @classmethod
    def update(cls, email, new_otp):
        user=settings.AUTH_USER_MODEL.objects.get(email=email)
        verification=cls.objects.filter(user=user).first()
        verification.otp=new_otp
        verification.timestamp=timezone.now()
        verification.save()
        
        return verification
    