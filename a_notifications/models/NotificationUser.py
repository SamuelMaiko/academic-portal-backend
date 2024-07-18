from django.conf import settings
from django.db import models

from api.models import BaseModel

from .Notification import Notification


class NotificationUser(BaseModel):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='notif_association')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notif_association')
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table='notification_user'
        unique_together = ('notification', 'user')

    def __str__(self):
        return f'{self.notification.message} - {self.user.username}'