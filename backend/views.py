from django.forms import ValidationError
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from backend.serializers import *
from rest_framework import viewsets, status
from django.contrib.auth.password_validation import validate_password
from .models import Profile
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db.models.query_utils import Q

# Create your views here.
class UserRegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.filter(is_active=True)
    
    @action(detail=False, methods=["POST"])
    def register(self, request):
        print("=====request Data")
        print(request.data)
        
        email = request.data.get("email")
        firstName = request.data.get("firstName")
        lastName = request.data.get("lastName")
        password = request.data.get("password")
        
        if not email or not firstName or not password:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'First name or Email address required'
                }
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {
                    'status': status.HTTP_409_CONFLICT,
                    'message': 'Email address already exists'
                }
            )
        
        baseUsername = f"{firstName}.{lastName}".lower()
        username = baseUsername
        num = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{username}{num}"
            num +=1
            
        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': str(e)
                }
            )
            
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            user.first_name = firstName
            user.last_name = lastName
            user.save()
            
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': f"{e}"
                }
            )
            
        user_profile, created = Profile.objects.get_or_create(user=user)
        
        user_profile.phone_number = "0657575755"
        user_profile.save()
        
        return Response(
            {
                'status': status.HTTP_201_CREATED,
                'message': 'User Created Success'
            }
        )
    
    
class LoginAPIView(APIView):
        def post(self, request, *args, **kwargs):
            email_or_username = request.data.get("email", "").strip()
            password = request.data.get("password", "").strip()

            user = User.objects.filter(Q(email=email_or_username) | Q(username=email_or_username)).first()

            if user:
                auth_user = authenticate(username=user.username, password=password)

                if auth_user:
                    refresh = RefreshToken.for_user(user)
                    serializer = LoginSerializer(user)  # Ensure this serializer is correctly implemented

                    # Optional: Update last login time
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])

                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Login Successfully",
                        "data": serializer.data,
                        "token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                        "expires_at": str(refresh.access_token.lifetime)
                    })
                else:
                    # If authenticate returns None, it's usually due to a wrong password
                    return Response({
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "Invalid username or password"
                    })
            else:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "User does not exist"
                })
        
    
