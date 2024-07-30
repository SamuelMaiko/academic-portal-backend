from api.models import BaseModel
from django.conf import settings
from django.db import models

from .Revision import Revision


class RevisionMessage(BaseModel):
    message = models.TextField(null=True, blank=True)
    file=models.FileField(upload_to='revision_message_files', null=True, blank=True)
    image=models.ImageField(upload_to='revision_message_images', null=True, blank=True)
    is_read=models.BooleanField(default=False)
    sender=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='revision_messages', null=True)
    revision=models.ForeignKey(Revision, on_delete=models.CASCADE, related_name='messages')

    class Meta:
        db_table = "revision_messages"  

    def __str__(self):
        return f'Revision message from {self.sender.registration_number if self.sender is not None else None} for work {self.revision.work.work_code}'
        