import emoji
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

    def save(self, *args, **kwargs):
        self.bio = self.convert_emojis_to_shortcodes(self.bio)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "profiles"  

    def __str__(self):
        return f'Profile of {self.user.registration_number}'
    
    
    # Convert shortcodes back to emojis after retrieving from the database
    @property
    def bio_with_emojis(self):
        return self.convert_shortcodes_to_emojis(self.bio)

    def convert_emojis_to_shortcodes(self, text):
        return emoji.demojize(text)

    def convert_shortcodes_to_emojis(self, text):
        return emoji.emojize(text, language='alias')