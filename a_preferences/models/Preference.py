from django.conf import settings
from django.db import models

from api.models import BaseModel


class Preference(BaseModel):
    dark_mode=models.BooleanField(default=False)
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preferences",
        )

    class Meta:
        db_table="preferences"

    def __str__(self):
        return f"{self.user.registration_number} preferences"