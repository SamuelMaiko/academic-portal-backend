from django.db import models
from django.conf import settings
from api.models import BaseModel 
import random
import string

class Work(BaseModel):
    WORK_CHOICES=[
        ('Essay', 'Essay'),
        ('Reflection Paper', 'Reflection_Paper'),
    ]
    STATUS_CHOICES=[
        ('Completed', 'Completed'),
        ('In Progress', 'In progress'),
        ('Not started', 'Not started'),
    ]
    
    work_code = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100,choices=WORK_CHOICES, default="Essay", blank=True)
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
    # has_writer = models.BooleanField(default=False)
    revoked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='RevokedWork', 
        related_name='revoked_work'
        )
    

    class Meta:
        db_table = "work"  

    def __str__(self):
        return f'Work {self.work_code}'
    
    @property
    def has_writer(self):
        return not ((self.assigned_to or self.uptaken_by) ==None)

    @property
    def writer(self):
        return self.assigned_to or self.uptaken_by  