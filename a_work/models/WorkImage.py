from django.db import models
from .Work import Work
from api.models import BaseModel
from cloudinary_storage.storage import MediaCloudinaryStorage 

class WorkImage(BaseModel):
    image=models.ImageField(upload_to='work_images', null=True, blank=True)
    work=models.ForeignKey(Work, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        storage=MediaCloudinaryStorage(), 
        upload_to='academic-portal/work-images/', 
        blank=True, 
        null=True
    )

    class Meta:
        db_table = "work_images"

    def __str__(self):
        return f'Image no. {self.pk} for {self.work.work_code}'