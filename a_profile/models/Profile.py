from api.models import BaseModel
from django.conf import settings
from django.db import models


class Profile(BaseModel):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    linkedin=models.URLField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        db_table = "profiles"  

    def __str__(self):
        return f'Profile of {self.user.registration_number}'