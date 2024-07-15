from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import Signal, receiver

send_welcome_email_signal=Signal()

@receiver(send_welcome_email_signal, sender=None)
def send_welcome_email_signal_handler(sender, **kwargs):
    user=kwargs["user"]
    
    subject="Welcome to 8 Tech Solutions - Email Verified Successfully!"
    message=f"""
    Hello {user.username},
    
    Congratulations! Your email address has been successfully verified.

    Welcome to 8 Tech Solutions, we're excited to have you on board!

    As a verified member, you now have full access to all the features and benefits our platform offers. Here are a few things you can do next:

    1. Explore Our Features: Discover tools and resources tailored to help you achieve your goals.
    2. Complete Your Profile: Enhance your experience by filling out your profile with more details [link to profile completion].
    If you have any questions or need assistance, feel free to reach out to our support team at support@8techsolutions.com.

    Thank you for joining us. We look forward to helping you achieve your goals with 8 Tech Solutions.

    Best regards,

    8 Tech Solutions Team.
    """
    sender=settings.EMAIL_HOST_USER
    recipient_list=[user.email]
    
    send_mail(subject, message, sender, recipient_list, fail_silently=True)