from django.db import models
from django.conf import settings
from a_work.models import Work
from api.models import BaseModel 

class RevokedWork(BaseModel):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    work=models.ForeignKey(Work, on_delete=models.CASCADE)

    class Meta:
        db_table = "revoked_works"  

    def __str__(self):
        return f'User {self.user.registration_number} reoked Work {self.work.work_code}'