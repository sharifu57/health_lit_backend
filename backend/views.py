from django.forms import ValidationError
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from backend.serializers import RegisterSerializer
from rest_framework import viewsets, status
from django.contrib.auth.password_validation import validate_password
from .models import Profile
from rest_framework.decorators import action

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
    
    
