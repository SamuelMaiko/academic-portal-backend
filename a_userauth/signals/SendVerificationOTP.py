from a_userauth.models import EmailOTP
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.dispatch import Signal, receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

send_verification_otp=Signal()

@receiver(send_verification_otp, sender=None)
def send_verification_otp_handler(sender, **kwargs):
    user=kwargs["user"]
    user_email=kwargs["email"]
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
    recipient_list=[user_email]
    
   # Define HTML content
    html_content = render_to_string('a_userauth/verify_email.html', {
        'registration_number': user.registration_number,
        'otp':otp
        })
    text_content = strip_tags(html_content) 
    
    email = EmailMultiAlternatives(subject, text_content, sender, recipient_list)
    
   # Attach the HTML content
    email.attach_alternative(html_content, "text/html")

    email.send()
    
    