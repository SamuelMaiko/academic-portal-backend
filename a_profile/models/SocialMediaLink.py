from django.db import models
from django.conf import settings
from api.models import BaseModel 
from .Profile import Profile

class SocialMediaLink(BaseModel):
    platform = models.CharField(max_length=100, blank=True)
    url = models.URLField()
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="social_media_links")

    class Meta:
        db_table = "social_media_links"  

    def __str__(self):
        return f'{self.platform} link for {self.profile.user.registration_number}'