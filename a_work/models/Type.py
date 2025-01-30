from django.conf import settings
from django.db import models

from api.models import BaseModel


class Type(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = "type"  
        ordering = ("-created_at",)

    def __str__(self):
        return f'Type {self.name}'
