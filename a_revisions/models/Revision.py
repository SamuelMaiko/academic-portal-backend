from django.db import models
from django.conf import settings
from a_work.models import Work
from api.models import BaseModel 

class Revision(BaseModel):
    STATUS_CHOICES=[
        ('Completed', 'Completed'),
        ('In Progress', 'In progress'),
        ('Not started', 'Not started'),
    ]
    work=models.ForeignKey(Work, on_delete=models.CASCADE, related_name='revisions')
    reviewer=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='revised_work')
    submit_before=models.DateTimeField()
    status = models.CharField(max_length=100,choices=STATUS_CHOICES, blank=True)
    is_open=models.BooleanField(default=False)

    class Meta:
        db_table = "revisions"  

    def __str__(self):
        return f'Revision for {self.work.work_code} by {self.reviewer.registration_number}'
        