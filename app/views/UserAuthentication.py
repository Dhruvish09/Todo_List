from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from django.contrib.auth import authenticate,logout
from app.renderers import CustomRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# Get tokens for a user


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegister(APIView):
    renderer_classes = [CustomRenderer]
    def post(self,request,formate=None):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Status":status.HTTP_201_CREATED,"Payload":serializer.data,"Message":"User created Successfully"})
            else:
                return Response({"Status":status.HTTP_400_BAD_REQUEST,"Error":serializer.errors})
        except Exception as e:
            return Response({"Status":status.HTTP_404_NOT_FOUND,"Error": e.detail})
        

class UserLogin(APIView):
    renderer_classes = [CustomRenderer]
    def post(self,request,formate=None):
        try:
            serializer = UserLoginSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                email = serializer.data.get('email')
                password = serializer.data.get('password')
                
                user = authenticate(email=email,password=password)
                if user is not None:
                    token = get_tokens_for_user(user)
                    return Response({"Status":status.HTTP_200_OK,"Token":token,"Message":"User logged in Successfully"})
                else:
                    return Response({'status':status.HTTP_404_NOT_FOUND,'errors':{'non_field_errors':['Email or Password is not Valid']}})
            else:
                return Response({"Status":status.HTTP_400_BAD_REQUEST,"Error":serializer.errors})
        except Exception as e:
            return Response({"Status":status.HTTP_404_NOT_FOUND,"Error": e.detail})
        
class UserProfile(APIView):
    renderer_classes = [CustomRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,formate=None):
            serializer = UserProfileSerializer(request.user)
            return Response({"Status":status.HTTP_200_OK,"Payload":serializer.data,"Message":"User Profile"})
    
class UserChangePassword(APIView):
    renderer_classes = [CustomRenderer]
    permission_classes = [IsAuthenticated]

    def post(self,request,formate=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"Status":status.HTTP_201_CREATED,"Payload":serializer.data,"Message":"Password changed Successfully"})
        else:
            return Response({"Status":status.HTTP_400_BAD_REQUEST,"Error":serializer.errors})
        
class UserLogout(APIView):
    renderer_classes = [CustomRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            logout(request)
            return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        