from django.conf import settings
from django.db import models

from a_work.models import Work
from api.models import BaseModel


class Notification(BaseModel):
    NOTIFICATION_TYPES = [
        ('Nearing Deadline', 'Nearing Deadline'),
        ('New Revision', 'New Revision'),
        ('Update Profile', 'Update Profile'),
        ('System Notification', 'System Notification'),
        ('Revoked Work', 'Revoked Work'),
        ('Uptaken Work', 'Uptaken Work'),
        ('Assigned Work', 'Assigned Work'),
    ]

    message = models.TextField()
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    triggered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='triggered_notifications'
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='notifications',
        through='NotificationUser',
        blank=True,
    )
    is_read = models.BooleanField(default=False)
    work = models.ForeignKey(
        Work, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        null=True, 
        blank=True, 
    )

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return f'Notification for {self.user.registration_number if self.user else None} - {self.get_type_display()}'
