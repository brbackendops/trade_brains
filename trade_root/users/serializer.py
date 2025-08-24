from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User

from .logger import log


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','designation','password']
        read_only_fields = ['is_active', 'is_superuser', 'is_staff']
        extra_kwargs = {
            "password": { "write_only": True }
        }
    
    def validate(self,data):
        if data["first_name"] is None:
            raise serializers.ValidationError("first_name is required")
        
        if data["last_name"] is None:
            raise serializers.ValidationError("last_name is required")
        
        if data["email"] is None:
            raise serializers.ValidationError("email is required")
        
        if data["password"] is None:
            raise serializers.ValidationError("password is required")
        
        return data


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    def validate(self,attrs):
        
        req = self.context.get('request')
        log.info(f"POST/{req.path} request received")
        
        email = attrs.get('email')
        password = attrs.get('password')
    
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                log.error(f"POST:{req.path} request ends in error: invalid credentials")
                raise serializers.ValidationError("Invalid Credentials ")
            
            if not user.is_active:
                log.error(f"POST:{req.path} request ends in error: user is not active")
                raise serializers.ValidationError("user is not active")
        else:
            log.error(f"POST:{req.path} request ends in error: required fields [email,password] are missing ")
            raise serializers.ValidationError("email and password fields are required")
        
        refresh = self.get_token(user)
        
        log.info(f"POST:{req.path} request successfull")
        return {
            "refresh": str(refresh),
            "access_token": str(refresh.access_token)
        }
    
    @classmethod
    def get_token(cls,user):
        
        token = super().get_token(user)

        token['email'] = user.email
        token['user_id'] = user.id
        
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token