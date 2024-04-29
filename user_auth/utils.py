import random
from datetime import datetime
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from .models import User,OneTimePassword
import base64
from django.conf import settings
# generate
class generateKey:
    @staticmethod
    def returnValue(email):
        return str(email) +  "Some Random Secret Key"



def send_code_otp(email):
    subject="Activate your account"
    try:
        user_instance = User.objects.get(email=email)
        
        try:
            OTPModel = OneTimePassword.objects.get(id=user_instance.id)
        except ObjectDoesNotExist:
            OTPModel = OneTimePassword.objects.create(id=user_instance.id)
       
    except ObjectDoesNotExist :
        # throw error
        raise ValueError("Email not found in database")
    OTPModel.counter += 1
    OTPModel.save()
    if OTPModel.counter >= 5:
        raise ValueError("You have exceeded the maximum number of otp attempts. You have been blocked from using the app")
    
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(email).encode()) 
    otp= pyotp.HOTP(key)
    otp_code=otp.at(OTPModel.counter)
    current_site = 'hyracorp.com'
    email_body = f'Hi {email}, Use the code {otp_code} to activate {current_site} your account'
    from_email=settings.DEFAULT_FROM_EMAIL
    send_email=EmailMessage(subject,email_body,from_email,[email])
    send_email.send(fail_silently=False)
def verify_otp(email,otp):
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        raise ValueError("Email not found in database")
    try:
        otp_model = OneTimePassword.objects.get(id=user.id)
    except ObjectDoesNotExist:
        raise ValueError("OTP not found in database")
    
    if otp_model.counter >= 5:
        raise ValueError("You have exceeded the maximum number of otp attempts. Please try again after some time")
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(email).encode()) 
    otpPy= pyotp.HOTP(key)
    
    if otpPy.verify(otp,otp_model.counter):
        otp_model.counter += 1
        otp_model.save()
        return True
    else:
        return False