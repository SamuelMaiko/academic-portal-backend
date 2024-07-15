from django.db import models
from django.conf import settings
from api.models import BaseModel 
from a_work.models import Work

class Submission(BaseModel):
    message = models.TextField()
    file=models.FileField(upload_to='submission_files')
    sender=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='submissions', null=True)
    work=models.ForeignKey(Work, on_delete=models.CASCADE, related_name='submissions')

    class Meta:
        db_table = "submissions"  

    def __str__(self):
        return f'Submission {self.pk} for work {self.work.work_code}'
        