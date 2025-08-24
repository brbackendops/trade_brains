from django.shortcuts import render

# rest_framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# serializer
from .serializer import UserSerializer , UserRegisterSerializer , CustomTokenObtainSerializer

# jwt
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.serializers import ValidationError

# model
from .models import User

# debug
from .logger import log

# views

class RegisterUserView(APIView):
    serializer_class = UserRegisterSerializer
    
    def post(self,request,*args,**kwargs):
        try:
            log.info(f"POST:{request.path} request received")
            body = request.data
            serializer = self.serializer_class(data=body)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            request.data.pop('password')
            
            log.info(f"POST:{request.path} request successfull")
            return Response(request.data,status=status.HTTP_201_CREATED)
        except ValidationError as err:
            log.error(f"POST:{request.path} request end in validation error: {err.detail}")
            return Response(
                {
                    "status": "error",
                    "name": err.__class__.__name__,
                    "error": err.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as err:
            log.error(f"POST:{request.path} request end in internal server error: {str(err)}")
            return Response({
                "status": "error",
                "name": err.__class__.__name__,
                "error": str(err),
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomJwtTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer