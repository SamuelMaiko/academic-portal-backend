from django.dispatch import receiver
from a_userauth.models import CustomUser
from a_profile.models import Profile
from django.db.models.signals import post_save

@receiver(post_save, sender=CustomUser)
def create_profile_signal_handler(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        