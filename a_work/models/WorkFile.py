from django.db import models
from .Work import Work
from api.models import BaseModel 

class WorkFile(BaseModel):
    file=models.FileField(upload_to='work_files')
    work=models.ForeignKey(Work, on_delete=models.CASCADE, related_name='files')

    class Meta:
        db_table = "work_files"  

    def __str__(self):
        return f'File no. {self.pk} for {self.work.work_code}'