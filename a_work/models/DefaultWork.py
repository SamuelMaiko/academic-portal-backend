from api.models import BaseModel
from django.db import models
from django.conf import settings
from a_work.models import Work

class DefaultWork(BaseModel):
    TYPE_CHOICES=[
        ('QualityIssues', 'Quality issues'),
        ('RevokedUptaken', 'Revoked Uptaken'),
        ('RevokedAssigned', 'Revoked Assigned'),
    ]
    
    type=models.CharField(max_length=20, choices=TYPE_CHOICES)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='default_work')
    work=models.ForeignKey(Work, on_delete=models.CASCADE, related_name='default_records')