from django.urls import path
from django.conf.urls import include
from twilio.rest import Client
from .views import ChangePasswordView, RegisterOtpView, RegisterView,ConfirmRegisterOtp,ForgetPassword,ConfirmForgetOtp
# from .views import RegisterWithEmailView
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

   path('register/',RegisterView.as_view(),name='register'),
  #  path('register/manager/',RegisterWithEmailView.as_view(),name='register-manager'),
  #path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('register/otp/', RegisterOtpView.as_view(), name='register-otp-verify'),
   path('register/confirmotp/',ConfirmRegisterOtp.as_view(),name='confirm-otp'),
  path('register/forget/',ForgetPassword.as_view(),name='forget-phone'),
  path('register/forget/otpconfirm/',ConfirmForgetOtp.as_view(),name='confirm-forget-otp'),
  
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('change_password/<int:pk>/',ChangePasswordView.as_view(),name='change-password'),
   
]

