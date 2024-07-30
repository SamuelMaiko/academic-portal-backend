from django.db import models
from django.conf import settings
from a_work.models import Work
from api.models import BaseModel 

class Bookmark(BaseModel):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    work=models.ForeignKey('a_work.Work', on_delete=models.CASCADE)

    class Meta:
        db_table = "bookmarks"  
        unique_together=('user', 'work')
        

    def __str__(self):
        return f'User {self.user.registration_number} bookmarks Work {self.work.work_code}'