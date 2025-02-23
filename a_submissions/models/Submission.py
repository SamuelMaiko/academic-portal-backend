from django.conf import settings
from django.db import models

from a_work.models import Work
from api.models import BaseModel
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class Submission(BaseModel):
    message = models.TextField()
    file = models.FileField(
        storage=RawMediaCloudinaryStorage(), 
        upload_to='academic-portal/submission-files/', 
        blank=True, 
        null=True
    )
    sender=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='submissions', null=True)
    work=models.ForeignKey(Work, on_delete=models.CASCADE, related_name='submissions')
    is_claimed=models.BooleanField(default=False)
    claimed_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='claimed_submissions',
        null=True,
        blank=True
        )

    class Meta:
        db_table = "submissions"  
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if self.claimed_by:
            self.is_claimed=True
        else:
            self.is_claimed=False
        return super().save( *args, **kwargs)

    def __str__(self):
        return f'Submission {self.pk} for work {self.work.work_code} by {self.sender.registration_number}'
        