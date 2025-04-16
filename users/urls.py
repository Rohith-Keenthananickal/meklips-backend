from django.urls import path
from .views import SignupView, LoginView, SendOTPView

urlpatterns = [
    path('register', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('send-otp', SendOTPView.as_view(), name='send-otp'),  
] 