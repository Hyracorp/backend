

# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from .models import User, OneTimePassword
import base64
from django.conf import settings

# GOAUTH
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

# generate


class generateKey:
    @staticmethod
    def returnValue(email):
        return str(email) + "Some Random Secret Key"


def send_code_otp(email,first_name=''):
    subject = "Activate your Hyracorp account"
    try:
        user_instance = User.objects.get(email=email)

        try:
            OTPModel = OneTimePassword.objects.get(id=user_instance.id)
        except ObjectDoesNotExist:
            OTPModel = OneTimePassword.objects.create(id=user_instance.id)

    except ObjectDoesNotExist:
        # throw error
        raise ValueError("Email not found in database")
    OTPModel.counter += 1
    OTPModel.save()
    if OTPModel.counter >= 5:
        raise ValueError(
            "You have exceeded the maximum number of otp attempts. You have been blocked from using the app")

    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(email).encode())
    otp = pyotp.HOTP(key)
    otp_code = otp.at(OTPModel.counter)
    current_site = 'hyracorp.com'
    app_url='https://app.hyracorp.com'
    # email_body = f'Hi {email}, Use the code {
    #     otp_code} to activate {current_site} your account'
   # HTML email content
    email_body_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
          <h2 style="color: #333;">Hello {first_name},</h2>
          <p style="font-size: 16px; color: #555;">
            We received a request to activate your account on <strong>{current_site}</strong>.
          </p>
          <p style="font-size: 16px; color: #555;">
            Please use the code below to complete your account activation:
          </p>
          <div style="text-align: center; margin: 20px 0;">
            <p style="font-size: 24px; font-weight: bold; color: #4CAF50; border: 1px solid #4CAF50; display: inline-block; padding: 10px 20px; border-radius: 5px;">{otp_code}</p>
            <p style="font-size: 16px; color: #555;"><a href="{app_url}/verify?email={email}&otp={otp_code}">Click here to activate your account</a></p>
          </div>
          <p style="font-size: 16px; color: #555;">
            If you did not request this code, please ignore this email.
          </p>
          <p style="font-size: 16px; color: #555;">
            Thank you,<br>
            The <strong>{current_site}</strong> Team
          </p>
        </div>
      </body>
    </html>
    """
    # Plain text email content (fallback)
    email_body_plaintext = f"""
    Hi {first_name},

    We received a request to activate your account on {current_site}.

    Please use the code below to complete your account activation:

    Your OTP Code: {otp_code}

    Click here to activate your account: {app_url}/verify?email={email}&otp={otp_code}

    If you did not request this code, please ignore this email.

    Thank you,
    The {current_site} Team
    """
    from_email = settings.DEFAULT_FROM_EMAIL

    send_email = EmailMultiAlternatives(subject, email_body_plaintext, from_email, [email])
    send_email.attach_alternative(email_body_html, "text/html")
    # send_email = EmailMessage(subject, email_body, from_email, [email])
    send_email.send(fail_silently=True)


def verify_otp(email, otp):
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        raise ValueError("Email not found in database")
    try:
        otp_model = OneTimePassword.objects.get(id=user.id)
    except ObjectDoesNotExist:
        raise ValueError("OTP not found in database")

    if otp_model.counter >= 5:
        raise ValueError(
            "You have exceeded the maximum number of otp attempts. Please try again after some time")
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(email).encode())
    otpPy = pyotp.HOTP(key)

    if otpPy.verify(otp, otp_model.counter):
        otp_model.counter += 1
        otp_model.save()
        return True
    else:
        return False


def send_transactional_email(data):
    subject = data['email_subject']
    email_body = data['email_body']
    from_email = settings.DEFAULT_FROM_EMAIL
    send_email = EmailMessage(
        subject, email_body, from_email, to=[data['to_email']])
    send_email.send(fail_silently=False)


class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(access_token, Request())

            return id_info

        except Exception as e:
            return f"token expired or invalid {e}"


def loginUser(email, password):
    login_user = authenticate(email=email, password=password)
    if login_user is not None:
        user_tokens = login_user.tokens()
        return {
            'email': login_user.email,
            'name': login_user.first_name,
            'access': user_tokens.get('access'),
            'refresh': user_tokens.get('refresh')
        }
    else:
        raise AuthenticationFailed('Invalid credentials')


def registerUser(provider, email, first_name, last_name):
    user = User.objects.filter(email=email)
    if user.exists():
        if provider == user[0].auth_provider:
            auth_user = loginUser(email, password=settings.SOCIAL_AUTH_PWD)
            return auth_user
        else:
            raise AuthenticationFailed(
                'Please continue your login using ' + user[0].auth_provider)
    else:
        newUser = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'auth_provider': provider,
        }

        reg_user = User.objects.create(**newUser)
        reg_user.set_password(settings.SOCIAL_AUTH_PWD)
        reg_user.is_verified = True
        reg_user.save()
        auth_user = loginUser(email, password=settings.SOCIAL_AUTH_PWD)
        return auth_user
