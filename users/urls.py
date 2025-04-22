from django.urls import path
from .views import SignupView, LoginView, SendOTPView, ValidateOTPView, PasswordResetView

urlpatterns = [
    path('register', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('forgot-password', SendOTPView.as_view(), name='send-otp'),
    path('validate-otp', ValidateOTPView.as_view(), name='validate-otp'),
    path('reset-password', PasswordResetView.as_view(), name='reset-password'),
]