from .GenerateOTP import generate_otp
from a_userauth.models import EmailOTP

def create_otp_model(user):
    otp=generate_otp()
    EmailOTP.objects.create(user=user, otp=otp)