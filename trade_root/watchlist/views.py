from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
# rest_framework

from rest_framework import generics , status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException


# models 
from trade_root.watchlist.models import WatchList
from trade_root.users.logger import log
from .models import WatchList

# serializers
from .serializer import WatchListRetrieveSerializer , WatchListCreateSerializer , WatchListAddSerializer , WatchListRemoveSerializer

# debugging
import traceback as tb
from .logger import log

class WatchListAPI(generics.ListAPIView):
    serializer_class = WatchListRetrieveSerializer    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        obj = WatchList.objects.filter(user=self.request.user)
        return obj
    
    
    def get(self,request,*args,**kwargs):
        try:
            log.info(f"GET:{request.path} request received ")
            qs = self.get_queryset()
            serializer = self.serializer_class(qs,many=True)
            log.info(f"GET:{request.path} data serialized successfully")
            # print(serializer.data)
            
            log.info(f"GET:{request.path} request successfull")
            return Response(
                {
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        except APIException as err:
            log.info(f"GET:{request.path} request end in Internal Server Error , [cause]: APIException , error: {str(err)}")
            return Response({
                "status": "error",
                "name": err.__class__.__name__,
                "error": err.detail,
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as err:
            # print(tb.print_tb(err.__traceback__))
            log.info(f"GET:{request.path} request end in Internal Server Error , [cause]: Exception , error: {str(err)}")
            return Response({
                "status": "error",
                "name": err.__class__.__name__,
                "error": str(err),
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class WatchListCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchListCreateSerializer
    
    def post(self,request,*args,**kwargs):
        try:
            log.info(f"POST:{request.path} request received ")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            log.info(f"POST:{request.path} request serialized successfully")
            self.perform_create(serializer)
            
            log.info(f"POST:{request.path} request  successfull")
            return Response(
                {
                    "status": "success"
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as err:
            log.info(f"POST:{request.path} request end in Internal Server Error , [cause]: Exception , error: {str(err)}")
            return Response({
                "status": "error",
                "name": err.__class__.__name__,
                "error": str(err),
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WatchListAdd(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = WatchListAddSerializer
    
    def post(self,request,*args,**kwargs):
        try:
            
            log.info(f"POST:{request.path} request received ")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            log.info(f"POST:{request.path} request serialized successfully")
            self.perform_create(serializer)            
            
            return Response(
                {
                    "status": "success",
                },
                status=status.HTTP_201_CREATED
            )
            
        except ObjectDoesNotExist as err:
            log.info(f"POST:{request.path} request end in Internal Server Error , [cause]: ObjectDoesNotExist , error: {str(err)}")
            return Response({
                "status": "error",
                "error_name": err.__class__.__name__,
                "error": str(err),
            },status=status.HTTP_404_NOT_FOUND)
            
        except Exception as err:
            log.info(f"POST:{request.path} request end in Internal Server Error , [cause]: Exception , error: {str(err)}")
            return Response({
                "status": "error",
                "name": err.__class__.__name__,
                "error": str(err),
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
            
class WatchListRemove(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = WatchListRemoveSerializer
    
    def post(self,request,*args,**kwargs):
        try:
            
            log.info(f"POST:{request.path} request received ")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            log.info(f"POST:{request.path} request serialized successfully")
            self.perform_create(serializer)       
            
               
            log.info(f"POST:{request.path} request successfully")
            return Response(
                {
                    "status": "success",
                },
                status=status.HTTP_201_CREATED
            )  
            
        except ObjectDoesNotExist as err:
            log.info(f"POST:{request.path} request end in Internal Server Error , [cause]: ObjectDoesNotExist , error: {str(err)}")
            return Response({
                "status": "error",
                "error_name": err.__class__.__name__,
                "error": str(err),
            },status=status.HTTP_404_NOT_FOUND)
            
        except Exception as err:
            log.info(f"POST:{request.path} request end in Internal Server Error , [cause]: Exception , error: {str(err)}")            
            return Response({
                "status": "error",
                "name": err.__class__.__name__,
                "error": str(err),
            })             