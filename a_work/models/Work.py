import random
import string

from django.conf import settings
from django.db import models

from api.models import BaseModel


class Work(BaseModel):
    STATUS_CHOICES=[
        ('Completed', 'Completed'),
        ('In Progress', 'In progress'),
        ('Not started', 'Not started'),
    ]
    
    work_code = models.CharField(max_length=100, null=True, blank=True)
    type = models.ForeignKey("type", on_delete=models.SET_NULL, related_name="work", null=True, blank=True, default=None)
    words = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=100,choices=STATUS_CHOICES, default="Not started", blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='authored_work',
        null=True,
        blank=True
        )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_work',
        null=True,
        blank=True
        )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        related_name='assign_work',
        null=True,
        blank=True
        )
    uptaken_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='uptaken_work',
        null=True,
        blank=True
        )
    is_submitted = models.BooleanField(default=False)
    # normalization required (later)
    uptaken_is_read = models.BooleanField(default=False)
    assigned_is_read = models.BooleanField(default=False)
    

    class Meta:
        db_table = "work"  
        ordering = ("-created_at",)

    def __str__(self):
        return f'Work {self.work_code}'
    
    @property
    def has_writer(self):
        return not ((self.assigned_to or self.uptaken_by) ==None)

    @property
    def writer(self):
        return self.assigned_to or self.uptaken_by  