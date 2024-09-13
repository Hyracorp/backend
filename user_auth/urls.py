from django.urls import path
from .views import RegisterUserView, VerifyUserView, LoginUserView, PasswordResetRequestView, SetNewPasswordView, PasswordResetConfirmView, GoogleSignInView, CookieTokenRefreshView,ResendOTPView

urlpatterns = [
    path('register', RegisterUserView.as_view(), name='register'),
    path('verify-email', VerifyUserView.as_view(), name='verify'),
    path('resend-otp', ResendOTPView.as_view(), name='resend-otp'),
    path('login', LoginUserView.as_view(), name='login'),
    path('refresh-token', CookieTokenRefreshView.as_view(), name='refresh-token'),
    path('google-login', GoogleSignInView.as_view(), name='google-login'),
    path('reset-password', PasswordResetRequestView.as_view(), name='reset-password'),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('set-new-password', SetNewPasswordView.as_view(), name='set-new-password'),
]
