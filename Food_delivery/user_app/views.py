# from django.shortcuts import render
# Create your views here.

from asyncio import exceptions
from multiprocessing.connection import Client
from typing import ContextManager
from django.shortcuts import render
from rest_framework import response
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.views import APIView
from .serializers import  ChangePasswordSerializer, RegisterWithEmailSerializer, UserRegister
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Account
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework import mixins,serializers,status
# Create your views here.
from django.http.response import Http404


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user_app.permissions import IsObjectOwner
from rest_framework.permissions import IsAuthenticated

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


from rest_framework.permissions import AllowAny
from .import transactions
from utilities import exceptions as authnz_exceptions




class RegisterView(generics.CreateAPIView):


    def get(self, request):
        users = Account.objects.all()
        serializer = UserRegister(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserRegister(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            request.session['phone_number'] = serializer.data['phone_number']
            return Response({
                "user": serializer.data,
                "message": "Registered Successfully"
            })
        else:
            return Response({
                "error": serializer.errors
            })

# class RegisterWithEmailView(generics.CreateAPIView):
#      permission_classes = [AllowAny, ]
#      serializer_class=RegisterWithEmailSerializer

#      def post(self, request, **kwargs):
#             try:
#                 serialized_data = self.serializer_class(data=request.data)
#                 if serialized_data.is_valid(raise_exception=True):
#                     email = serialized_data.data['email'].lower()
#                     password = request.data['password']
#                     try:
#                         user = User.objects.get(email=email)

#                     except Account.DoesNotExist as e:
#                         user = None
#                     if user:
#                         raise authnz_exceptions.CustomException(detail='This email is registered before.')
#                     else:
#                         RegisterWithEmailSerializer(data=request.data)
#                         transactions.register_user_with_email_and_password(email, password)
#                         return Response(status=status.HTTP_200_OK)
#             except authnz_exceptions.CustomException as e:
#                 return Response(status=e.status_code)
#             except exceptions.ValidationError as e:
#                 return Response(status=e.status_code)


   
 

class ChangePasswordView(generics.UpdateAPIView,Exception):
    queryset=Account.objects.all()
    permission_classes=[IsAuthenticated,IsObjectOwner]
    serializer_class = ChangePasswordSerializer
    

class RegisterOtpView(APIView):


    # def post(self,request):
    #     data=request.data
    #     phone_number = data['phone_number']

    #     try:
    #         account_sid='ACf9573b4828f0151c6af5904a4e31604e'
    #         auth_token='b2816325f712ad56f772a8b46830be02'
    #         client=Client(account_sid,auth_token)

    #         verification = client.verify \
    #                  .services('VA061ae5f0a6ce7574c9441a87fd2a74bb') \
    #                  .verifications \
    #                  .create(to='+91'+phone_number, channel='sms')

    #         return Response({   
    #             "success": "Otp send successfully"
    #         })
    #     except TwilioRestException:
    #         return Response({
    #             "error": "Not a valid phone number"
    #         })

    def get(self, request):


        if 'phone_number' in request.session:
            phone_number = request.session['phone_number']
        elif Account.objects.filter(email = request.user).exists():
            user = Account.objects.get(email = request.user)
            phone_number = user.phone_number
        else:
            return Response({
                "error": "Phone number not found"
            })
        account_sid ='ACf9573b4828f0151c6af5904a4e31604e'
        auth_token = 'b2816325f712ad56f772a8b46830be02'
        client = Client(account_sid, auth_token)

        try:
            client.verify \
                .services ('VA061ae5f0a6ce7574c9441a87fd2a74bb')\
                .verifications \
                .create(to='+91'+phone_number, channel='sms')

            return Response({
                "success": "Otp send successfully"
        })
        except TwilioRestException:
            return Response({
                "error": "some error occured"
            })



    def post(self, request):
        
        if 'phone_number' in request.session:
            phone_number = request.session['phone_number']
        elif Account.objects.filter(email = request.user).exists():
            user = Account.objects.get(email = request.user)
            phone_number = user.phone_number
        else:
            return Response({
                "error": "Phone number x not found"
            })

        data = request.data
        otp = data['otp']

        account_sid ='ACf9573b4828f0151c6af5904a4e31604e'
        auth_token ='b2816325f712ad56f772a8b46830be02'
        client = Client(account_sid, auth_token)

        try:
            verification_check = client.verify \
                .services('VA061ae5f0a6ce7574c9441a87fd2a74bb') \
                .verification_checks \
                .create(to='+91'+phone_number, code=otp)

            if verification_check.status == 'approved':
                user = Account.objects.get(phone_number=phone_number)
                user.is_verified = True
                user.save()

                if request.session['phone_number']:
                    del request.session['phone_number']
                else:
                    pass
                
                return Response({
                    "success":"otp verified"
                })
            else:
                return Response({
                    "error": "otp not matching"
                })

        except TwilioRestException:
            return Response({
                "error": "some error occured"
            })

class ConfirmRegisterOtp(APIView):
    
    def post(self,request):
        data=request.data
        phone_number=data['phone_number']
        otp=data['otp']

        account_sid='ACf9573b4828f0151c6af5904a4e31604e'
        auth_token='b2816325f712ad56f772a8b46830be02'
        client=Client(account_sid,auth_token)

        verification_check =client.verify \
            .services('VA061ae5f0a6ce7574c9441a87fd2a74bb') \
            .verification_checks \
            .create(to='+91'+phone_number, code=otp)

        if verification_check.status=='approved':
            try:
                user=Account.objects.get(phone_number=phone_number)
                user.is_verified =True
                user.save()
            except TwilioRestException:
                return Response({
                    "error": "Not a valid phone number"
                })

            return Response({
                "success":"otp verified"
            })
        else:

            return Response({
                "error":"otp not matching"
            })



class ForgetPassword(APIView):
    
    def post(self,request):
        data=request.data
        phone_number=data['phone_number']

        if Account.objects.filter(phone_number=phone_number):

            account_sid='ACf9573b4828f0151c6af5904a4e31604e'
            auth_token='b2816325f712ad56f772a8b46830be02'
            client=Client(account_sid,auth_token)

            try:
                client.verify\
                    .services('VA061ae5f0a6ce7574c9441a87fd2a74bb')\
                    .verifications\
                    .create(to='+91'+phone_number, channel='sms')
                return Response({
                    "success": "Otp send successfully"
                })
            except TwilioRestException:
                return Response({
                    "error": "some error occured"
                })

        else:
            return Response({
                "error": "Phone Number is not registered"
            })

class ConfirmForgetOtp(APIView):

    def post(self, request):

        data = request.data
        phone_number = data['phone_number']
        otp = data['otp']

        account_sid = 'ACf9573b4828f0151c6af5904a4e31604e'
        auth_token = 'b2816325f712ad56f772a8b46830be02'
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
            .services ('VA061ae5f0a6ce7574c9441a87fd2a74bb')\
            .verification_checks \
            .create(to='+91'+phone_number, code=otp)

        if verification_check.status == 'approved':
            user = Account.objects.get(phone_number=phone_number)
            user.is_verified = True
            user.save()

            return Response({
                "success":"otp verified"
            })
        else:
            return Response({
                "error": "otp not matching"
            })







# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['username'] = self.user.username
#         # data['fullname'] = self.user.fullname
#         data['email'] = self.user.email
#         # data['phone'] = self.user.phone
#         data['id']=self.user.id
#         return data


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

#reg
   # serializer_class = UserRegister
    # # parser_classes = [MultiPartParser, FormParser]
    
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception = True)
    #     user=serializer.save()
    #     return Response({"user": UserRegister(user,context=self.get_serializer_context()).data,
    #     "message":" Registered Successfully"})