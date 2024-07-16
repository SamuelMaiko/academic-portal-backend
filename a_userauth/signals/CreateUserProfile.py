from django.dispatch import receiver
from a_userauth.models import CustomUser, EmailOTP
from a_onboarding.models import Onboarding
from a_profile.models import Profile, SocialMediaLink
from django.db.models.signals import post_save
from a_userauth.HelperFunctions import generate_otp

@receiver(post_save, sender=CustomUser)
def create_profile_signal_handler(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        EmailOTP.objects.create(user=instance, otp=generate_otp())
        Onboarding.objects.create(user=instance)
        SocialMediaLink.objects.create(profile=instance.profile,platform='LinkedIn')
        