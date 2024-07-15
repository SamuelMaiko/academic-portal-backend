from django.db import models
from .Work import Work
from api.models import BaseModel 

class WorkImage(BaseModel):
    file=models.FileField(upload_to='work_images')
    work=models.ForeignKey(Work, on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = "work_images"  

    def __str__(self):
        return f'Image no. {self.pk} for {self.work.work_code}'