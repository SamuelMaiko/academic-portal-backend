from django.dispatch import Signal, receiver
from a_userauth.models import EmailOTP
from django.core.mail import send_mail
from django.conf import settings

send_otp_signal=Signal()

@receiver(send_otp_signal, sender=None)
def send_otp_signal_handler(sender, **kwargs):
    user=kwargs["user"]
    type=kwargs["type"]
    otp=EmailOTP.objects.filter(user=user).first().otp

    if type=="new_otp_request":
        subject = 'Password Reset Request - Your New OTP Code'
        message = f"Hi {user.first_name or user.email.split('@')[0] or user.registration_number},\n\nYou have requested a new OTP to reset your password. Use the following OTP code to reset your password:\n\n{otp}\n\nIf you did not request this, please ignore this email.\n\nBest regards,\nTechWave Team"
    elif type=="first_time_request":
        subject = 'Password Reset Request - Your OTP Code'
        message = f"Hi {user.first_name or user.email.split('@')[0] or user.registration_number},\n\nYou have requested to reset your password. Use the following OTP code to reset your password:\n\n{otp}\n\nIf you did not request this, please ignore this email.\n\nBest regards,\nTechWave Team"
    sender=settings.EMAIL_HOST_USER
    recipient_list=[user.email]
    
    send_mail(subject, message, sender, recipient_list, fail_silently=False)
    