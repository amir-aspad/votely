# import from rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# import from django
from django.contrib.auth import authenticate, get_user_model

# import from rest_framework_simplejwt
from rest_framework_simplejwt.tokens import RefreshToken

# import from panel
from .serializers import (
    LoginUserSerializer,
    RegisterUserSerializer,
    VerifyPhoneCodeSerializer
)
from .models import OTP


# other import
from utils.send_code import send_phone_verification_code
from random import randint


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        if serializer.is_valid():
            vd = serializer.validated_data

            user = authenticate(request, phone=vd['info'], password=vd['password'])
            if user is not None:
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterUserView(APIView):
    def post(self, request):
        ser_data = RegisterUserSerializer(data=request.data)

        if ser_data.is_valid():
            code = randint(100000, 999999)
            vd = ser_data.validated_data
            phone = vd['phone']

            # save info in session
            request.session['user_registration_info'] = {
                'phone': phone,
                'password': vd['password'],
            }

            # save code in otp model
            OTP.objects.update_or_create(
                phone=phone,
                defaults={'code': code}
            )
            # send code for user phone number
            send_phone_verification_code(phone=phone, code=code)
            
            return Response({'detail': 'Code successfully sent'}, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RegisterVerifyCodeView(APIView):
    def post(self, request):
        ser_data = VerifyPhoneCodeSerializer(data=request.data)
        
        if ser_data.is_valid():
            vd = ser_data.validated_data
            data = request.session.get('user_registration_info')
            
            if not data:
                return Response({'detail': 'Session expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                otp_code = OTP.objects.get(phone=data['phone'], code=vd['code'])

                if not otp_code.is_expired():
                    User = get_user_model()
                    User.objects.create_user(
                        phone=data['phone'],
                        password=data['password'],
                        is_phone_verified=True
                    )

                    # delete session and otp code in model
                    del request.session['user_registration_info']
                    otp_code.delete()

                    return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)
                return Response({'detail': 'Code has expired'}, status=status.HTTP_400_BAD_REQUEST)
            except OTP.DoesNotExist:
                return Response({'detail': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)