import emoji
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

    def save(self, *args, **kwargs):
        self.message = self.convert_emojis_to_shortcodes(self.message if self.message else "")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "revision_messages"  

      # Convert shortcodes back to emojis after retrieving from the database
    @property
    def message_with_emojis(self):
        return self.convert_shortcodes_to_emojis(self.message if self.message else "")

    def convert_emojis_to_shortcodes(self, text):
        return emoji.demojize(text)

    def convert_shortcodes_to_emojis(self, text):
        return emoji.emojize(text, language='alias')

    def __str__(self):
        return f'Revision message from {self.sender.registration_number if self.sender is not None else None} for work {self.revision.work.work_code}'
        