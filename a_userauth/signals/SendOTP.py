from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.dispatch import Signal, receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from a_userauth.models import EmailOTP

send_otp_signal=Signal()

@receiver(send_otp_signal, sender=None)
def send_otp_signal_handler(sender, **kwargs):
    user=kwargs["user"]
    type=kwargs["type"]
    otp=EmailOTP.objects.filter(user=user).first().otp

    if type=="new_otp_request":
        subject = 'Password Reset Request - Your New OTP Code'
        
    elif type=="first_time_request":
        subject = 'Password Reset Request - Your OTP Code'

    sender=settings.EMAIL_HOST_USER
    recipient_list=[user.email]
    
    # Define HTML content
    html_content = render_to_string('a_userauth/first_otp_reset_email.html', {
        'user': user,
        'otp': otp
        })
    text_content = strip_tags(html_content)  # Convert HTML to plain text
    
    email = EmailMultiAlternatives(subject, text_content, sender, recipient_list)
    
   # Attach the HTML content
    email.attach_alternative(html_content, "text/html")

    email.send()    
    