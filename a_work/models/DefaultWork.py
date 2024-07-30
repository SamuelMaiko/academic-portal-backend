from django.conf import settings
from django.db import models

from api.models import BaseModel

from .Work import Work


class DefaultWork(BaseModel):
    TYPE_CHOICES=[
        ('QualityIssues', 'Quality issues'),
        ('RevokedUptaken', 'Revoked Uptaken'),
        ('RevokedAssigned', 'Revoked Assigned'),
    ]
    
    type=models.CharField(max_length=20, choices=TYPE_CHOICES)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='default_work')
    work=models.ForeignKey(Work, on_delete=models.CASCADE, related_name='default_records')
    
    class Meta:
        db_table = "default_work"  
        ordering = ("-created_at",)

    def __str__(self):
        return f'User {self.user.registration_number} defaults {self.work.work_code} -{self.type}'