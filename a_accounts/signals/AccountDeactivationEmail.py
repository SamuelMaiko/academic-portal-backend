# signals.py
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal, receiver

account_deactivated = Signal()

@receiver(account_deactivated, sender=None)
def send_account_deactivation_email(sender, **kwargs):
    user = kwargs["user"]
    reason = kwargs["reason"]

    subject = "Your Account Has Been Deactivated"
    message = f"""
    Hello {user.first_name or user.registration_number},

    We wanted to inform you that your account with the email {user.email} has been deactivated by an administrator.

    Reason for deactivation: {reason}

    If you believe this is a mistake or if you have any questions, please contact our support team at techwave@gmail.com.

    Thank you,
    Techwave Team
    """
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)