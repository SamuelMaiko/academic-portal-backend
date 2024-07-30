# signals.py
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal, receiver

account_activated = Signal()

@receiver(account_activated, sender=None)
def send_account_activation_email(sender, **kwargs):
    user = kwargs["user"]
    
    subject = "Your Account Has Been Activated"
    message = """
    Hello,

    We are pleased to inform you that your account has been successfully activated.

    You can now log in to your account using your registraton number and password.

    If you have any questions or need further assistance, please feel free to contact our support team techwave@gmai.com.

    Welcome to Techwave Writers!

    Regards,
    Techwave Team
    """

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)