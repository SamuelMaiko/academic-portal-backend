# signals.py
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal, receiver

password_reset_signal = Signal()

@receiver(password_reset_signal, sender=None)
def handle_password_reset(sender, **kwargs):
    user = kwargs['user']
    new_password = kwargs['new_password']

    subject = 'Password Reset Notification'
    message = f"""
    Hello,

    Your password has been reset successfully. Please use the following temporary password to log in:

    New Password: {new_password}

    After logging in, we recommend you to change your password immediately.

    Thank you,
    Techwave Team
    """

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
