from django.dispatch import Signal, receiver
from django.core.mail import send_mail
from django.conf import settings

email_account_credentials=Signal()

@receiver(email_account_credentials, sender=None)
def email_account_credentials_handler(sender, **kwargs):
    registration_number=kwargs["registration_number"]
    password=kwargs["password"]
    email=kwargs["email"]
    
    subject = f"Account Details for {registration_number}"

    message = f"Hello,\n\n" \
              f"Your registration details:\n" \
              f"Registration Number: {registration_number}\n" \
              f"Password: {password}\n\n" \
              f"Please keep this information secure.\n\n" \
              f"Thank you,\n" \
              f"TechWave Team"

    sender=settings.EMAIL_HOST_USER
    recipient_list=[email, 'samuel.maiko@student.moringaschool.com']

    send_mail(subject, message, sender, recipient_list, fail_silently=False)

    

    