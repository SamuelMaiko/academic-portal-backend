from django.db import models
from django.conf import settings
from api.models import BaseModel 

class Work(BaseModel):
    WORK_CHOICES=[
        ('Essay', 'Essay'),
        ('Reflection', 'Reflection_Paper'),
    ]
    STATUS_CHOICES=[
        ('Completed', 'Completed'),
        ('In Progress', 'In progress'),
        ('Not started', 'Not started'),
    ]
    
    work_code = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100,choices=WORK_CHOICES, blank=True)
    words = models.IntegerField()
    comment = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=100,choices=STATUS_CHOICES, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='authored_work', null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='assigned_work', null=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='assign_work', null=True)
    uptaken_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='uptaken_work', null=True)
    is_submitted = models.BooleanField(default=False)
    has_writer = models.BooleanField(default=False)
    revoked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='RevokedWork', 
        related_name='revoked_work'
        )
    bookmarked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='Bookmark', 
        related_name='bookmarks'
        )

    class Meta:
        db_table = "work"  

    def __str__(self):
        return f'Work {self.work_code}'