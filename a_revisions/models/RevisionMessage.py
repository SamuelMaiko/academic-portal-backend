from django.db import models
from django.conf import settings
from api.models import BaseModel 
from .Revision import Revision

class RevisionMessage(BaseModel):
    message = models.TextField()
    file=models.FileField(upload_to='revision_message_files')
    image=models.ImageField(upload_to='revision_message_images')
    is_read=models.BooleanField(default=False)
    sender=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='revision_messages', null=True)
    revision=models.ForeignKey(Revision, on_delete=models.CASCADE, related_name='messages')

    class Meta:
        db_table = "revision_messages"  

    def __str__(self):
        return f'Revision message from {self.sender.registration_number} for work {self.revision.work.work_code}'
        