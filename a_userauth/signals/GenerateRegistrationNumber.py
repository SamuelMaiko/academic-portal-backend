from django.dispatch import receiver
from django.db.models.signals import post_save
from a_userauth.models import CustomUser
import random
import string

@receiver(post_save, sender=CustomUser)
def generate_reg_no_handler(sender, created, instance, **kwargs):
    if created:
        instance.registration_number=generate_reg_no(instance.pk)
        instance.save()

def generate_reg_no(pk):
    random_digits = ''.join(random.choices(string.digits, k=2))
    return f'TW{random_digits}0{pk}'