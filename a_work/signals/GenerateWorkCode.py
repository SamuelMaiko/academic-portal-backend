from django.dispatch import receiver
from django.db.models.signals import post_save
from a_work.models import Work
import random
import string

@receiver(post_save, sender=Work)
def generate_work_code_handler(sender, created, instance, **kwargs):
    if created:
        instance.work_code=generate_work_code(instance.pk)
        instance.save()

def generate_work_code(pk):
        random_digits = ''.join(random.choices(string.digits, k=2))
        return f'WK{random_digits}0{pk}'