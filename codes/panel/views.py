# import from rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# import from django
from django.contrib.auth import authenticate

# import from rest_framework_simplejwt
from rest_framework_simplejwt.tokens import RefreshToken

# import from panel
from .serializers import LoginUserSerializers


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginUserSerializers(data=request.data)

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