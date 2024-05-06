import random
from datetime import datetime
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from .models import User,OneTimePassword
import base64
from django.conf import settings

# GOAUTH
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

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
    send_email.send(fail_silently=True)
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
def send_transactional_email(data):
    subject=data['email_subject']
    email_body=data['email_body']
    from_email=settings.DEFAULT_FROM_EMAIL
    send_email=EmailMessage(subject,email_body,from_email,to=[data['to_email']])
    send_email.send(fail_silently=False)
    



class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info=id_token.verify_oauth2_token(access_token,Request())

            return id_info
        
        except Exception as e:
            return "token expired or invalid"
        
def loginUser(email,password):
    login_user = authenticate(email=email, password=password)
    if login_user is not None:
        user_tokens=login_user.tokens()
        return {
            'email':login_user.email,
            'name':login_user.first_name,
            'access':user_tokens.get('access'),
            'refresh':user_tokens.get('refresh')    
        }
    else:
        raise AuthenticationFailed('Invalid credentials')

def registerUser(provider,email,first_name,last_name):
        user = User.objects.filter(email=email)
        if user.exists():
            if provider == user[0].auth_provider:
                auth_user=loginUser(email,password=settings.SOCIAL_AUTH_PWD)
                return auth_user
            else:
                raise AuthenticationFailed('Please continue your login using ' + user[0].auth_provider)
        else:
            newUser={
                'email':email,
                'first_name':first_name,
                'last_name':last_name,
                'auth_provider':provider,    
            }
            
            reg_user=User.objects.create(**newUser)
            reg_user.set_password(settings.SOCIAL_AUTH_PWD)
            reg_user.is_verified=True
            reg_user.save()
            auth_user=loginUser(email,password=settings.SOCIAL_AUTH_PWD)
            return auth_user