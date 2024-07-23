from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.dispatch import Signal, receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

email_account_credentials=Signal()

@receiver(email_account_credentials, sender=None)
def email_account_credentials_handler(sender, **kwargs):
    registration_number=kwargs["registration_number"]
    password=kwargs["password"]
    receiver=kwargs["email"]
    
    subject = f"Account Details for {registration_number}"

    # message = f"Hello,\n\n" \
    #           f"Your registration details:\n" \
    #           f"Registration Number: {registration_number}\n" \
    #           f"Password: {password}\n\n" \
    #           f"Please keep this information secure.\n\n" \
    #           f"Thank you,\n" \
    #           f"TechWave Team"

    sender=settings.EMAIL_HOST_USER
    recipient_list=[receiver]

    # Define HTML content
    html_content = render_to_string('a_userauth/welcome_email_template.html', {
        'registration_number': registration_number,
        'password':password
        })
    text_content = strip_tags(html_content) 
    
    email = EmailMultiAlternatives(subject, text_content, sender, recipient_list)
    
   # Attach the HTML content
    email.attach_alternative(html_content, "text/html")

    email.send()

    

    