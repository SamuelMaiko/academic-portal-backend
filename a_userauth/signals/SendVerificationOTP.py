from django.dispatch import Signal, receiver
from a_userauth.models import EmailOTP
from django.core.mail import send_mail
from django.conf import settings

send_verification_otp=Signal()

@receiver(send_verification_otp, sender=None)
def send_verification_otp_handler(sender, **kwargs):
    user=kwargs["user"]
    otp=EmailOTP.objects.filter(user=user).first().otp

    subject = "OTP for Email Verification"

    message = f"""
    Hello,

    Your OTP (One-Time Password) for account verification is: {otp}

    Please use this OTP to verify your account.

    If you did not request this OTP, please disregard this email.

    Regards,
    Techwave Writers Team
    """
    sender=settings.EMAIL_HOST_USER
    recipient_list=[user.email]
    
    send_mail(subject, message, sender, recipient_list, fail_silently=False)
    
    