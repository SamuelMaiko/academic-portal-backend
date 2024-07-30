from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal, receiver

send_account_deletion_email = Signal()

@receiver(send_account_deletion_email, sender=None)
def send_account_deletion_email_handler(sender, **kwargs):
    user = kwargs["user"]
    subject = "Your Account Has Been Deleted"
    message = f"""
    Hello {user.first_name or user.registration_number},

    We regret to inform you that your account with the email {user.email} has been deleted by an administrator.

    If you have any questions or believe this is a mistake, please contact our support team at techwave@gmail.com.

    Regards,
    Techwave Writers Team
    """
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)