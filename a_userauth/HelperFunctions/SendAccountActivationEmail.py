from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
                               
def SendAccountActivationEmail(user, request):
    subject="Our Dating App Activation"
        
    domain=get_current_site(request).domain
    
    token=Token.objects.create(user=user)
    
    uid64=urlsafe_base64_encode(force_bytes(user.pk))
    
    
    context={
        'user':user,
        'domain':domain,
        'token':token.key,
        'uid64':uid64,
    }
    message=render_to_string('userauth/account_activation.html',context)
    sender=settings.EMAIL_HOST_USER
    recipient_list=[user.email]
    
    email=EmailMessage(subject, message, sender, recipient_list)
    email.fail_silently=True
    email.send()