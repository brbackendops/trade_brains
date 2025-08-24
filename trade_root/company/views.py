from django.shortcuts import render
from django.forms.models import model_to_dict

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import APIException

# serializer
from trade_root.company.models import CompanyInfo
from .serializer import CompanyRetrieveSerializer , CompanyCreationSerilalizer , CompanyInfoSerializer

# models
from .models import Company

# debuggin
from .logger import log

# views

class CompanyListView(APIView):
    
    serializer_class = CompanyRetrieveSerializer
    model = Company
    

    def get_queryset(self) -> object | None:
        obj =  self.model.objects.all()
                    
        if obj is None:
            return None
        return obj
        
    
    def get(self,request,*args,**kwargs):
        try:
            
            log.info(f"GET:{request.path} request received ")
            companies = self.get_queryset()
                
            if companies is None:
                return Response(
                    {
                        "status": "success",
                        "data": []
                    },status=status.HTTP_200_OK
                )
                
            if 'name' in request.query_params:
                log.info(f"GET:{request.path} request goes for query with name value ")
                value = request.query_params['name']
                companies = companies.all().filter(companyy_name__icontains=value)
            
            
            if 'sort' in request.query_params:
                log.info(f"GET:{request.path} request goes for query with sort value ")
                value = request.query_params['sort']
                
                if value == 'desc':
                    log.info(f"GET:{request.path} request goes for query with sort with desc value ")
                    companies = companies.order_by('-created_at')
                
                if value == 'asc':
                    log.info(f"GET:{request.path} request goes for query with sort with asc value ")
                    companies = companies.order_by('created_at')
            

            serializer = self.serializer_class(companies,many=True)
            log.info(f"GET:{request.path} request successfull")
            
            return Response(
                {
                    "status": "success",
                    "data": serializer.data
                },status=status.HTTP_200_OK
            )            
            
        except Exception as err:
            log.error(f"GET:{request.path} request ends in error: {str(err)}")
            return Response({
                "status": "error",
                "error_name": err.__class__.__name__,
                "error": str(err),
                "cause": err.__cause__,
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanyCreationSerilalizer

    def create(self,request,*args,**kwargs):
        try:
            
            log.info(f"POST:{request.path} request received ")
            serializer = self.get_serializer(data=request.data)            
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            log.info(f"POST:{request.path} request successfull")
            return Response(
                {
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except APIException as err:
            log.error(f"POST:{request.path} request ends in , [cause]: APIException ,  error: {str(err)}")
            return Response({
                "status": "error",
                "error_name": err.__class__.__name__,
                "error": err.detail,
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                                
        except Exception as err:                        
            log.error(f"POST:{request.path} request ends in , [cause]: Exception ,  error: {str(err)}")
            return Response({
                "status": "error",
                "error_name": err.__class__.__name__,
                "error": str(err),
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompanyUpdateInfoView(APIView):
    
    def put(self,request,company_id):
        try:
            
            log.info(f"PUT:{request.path} request received")
            company = Company.objects.get(pk=company_id)
            if not company:
                raise Exception("model[company] not found")
            
            body = request.data
            body.update({ "company_id": company })
            
            company_is_exists = CompanyInfo.objects.filter(company_id=company.id).exists()
            log.info(f"PUT:{request.path} request resolved successfully in checking company exists or not")
            if not company_is_exists:                
                log.info(f"PUT:{request.path} request found company does not exists")                
                
                company_info = CompanyInfo.objects.create(**body)
                                
                log.info(f"PUT:{request.path} request created company_info successfully")
                return Response(
                    {
                        "status": "success",
                        "data": model_to_dict(company_info)
                    },
                    status=status.HTTP_200_OK
                )                
            
            company_info = CompanyInfo.objects.filter(company_id=company.id).first()
            company_info.symbol = body.get("symbol")
            company_info.scrip_code = body.get("scrip_code")
            company_info.save()
            
            log.info(f"PUT:{request.path} request updated company_info successfully")
            return Response(
                {
                    "status": "success",
                    "data": request.data
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as err:
            log.error(f"PUT:{request.path} request ends in , [cause]: Exception , error: {str(err)}")
            return Response({
                "status": "error",
                "error_name": err.__class__.__name__,
                "error": str(err),
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)