

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

# rest_framework
from rest_framework import serializers
from rest_framework.exceptions import APIException

# model
from .models import WatchList
from ..company.models import CompanyInfo , Company


# debugging
import traceback as tb


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']


class CompanyInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyInfo
        exclude = ['company_id']
    
class CompanySerializer(serializers.ModelSerializer):
    company_info = CompanyInfoSerializer(read_only=True)
    class Meta:
        model = Company
        fields = ['companyy_name','company_info']


class WatchListRetrieveSerializer(serializers.ModelSerializer):
    
    company = CompanySerializer(many=True,read_only=True)
    
    class Meta:
        model = WatchList
        fields = ['id','name','company']

class WatchListCreateSerializer(serializers.ModelSerializer):
        
        
    class Meta:
        model = WatchList
        fields = ['name']


    def create(self,validated_data):
        try:
            
            request = self.context.get('request')
            current_user = request.user
            
            new_watchlist = WatchList.objects.create(**validated_data, user=current_user)
            new_watchlist.save()
            
            return new_watchlist
            
        except Exception as err:
            raise serializers.ValidationError({
                "error": str(err),
                "name": err.__class__.__name__
            })

class WatchListAddSerializer(serializers.ModelSerializer):
    
    company_code = serializers.CharField(write_only=True)
    
        
    class Meta:
        model = WatchList
        fields = ['company_code']


    def create(self,validated_data):
        try:

            request = self.context.get('request')
            current_user = request.user
            
            watchlist_id = request.parser_context.get("kwargs").get("id")
            watchlist_obj = WatchList.objects.get(id=watchlist_id,user=current_user)
            if not watchlist_obj:
                raise ObjectDoesNotExist("watchlist not found")
            
            # print("watchlist",watchlist_obj)
            company_info_obj = CompanyInfo.objects.get(scrip_code=validated_data.get('company_code'))
            if not company_info_obj:
                raise ObjectDoesNotExist("company info not found")

            # print("company",company_info_obj)
            company = Company.objects.get(id=company_info_obj.company_id.id)
            if not company:
                raise ObjectDoesNotExist("company not found")
            
            # print("company from company obj", company)
            # print("watchlist",watchlist_obj)
            watchlist_obj.company.add(company)
            watchlist_obj.save()
            
            return watchlist_obj
            
        except Exception as err:
            # print(tb.print_tb(err.__traceback__))
            raise serializers.APIException({
                "error": str(err),
                "name": err.__class__.__name__
            })

class WatchListRemoveSerializer(serializers.ModelSerializer):

    company_code = serializers.CharField(write_only=True)
    
        
    class Meta:
        model = WatchList
        fields = ['company_code']        
        


    def create(self,validated_data):
        try:

            request = self.context.get('request')
            current_user = request.user
            
            watchlist_id = request.parser_context.get("kwargs").get("id")
            watchlist_obj = WatchList.objects.get(id=watchlist_id,user=current_user)
            if not watchlist_obj:
                raise ObjectDoesNotExist("watchlist not found")
            
            # print("watchlist",watchlist_obj)
            company_info_obj = CompanyInfo.objects.get(scrip_code=validated_data.get('company_code'))
            if not company_info_obj:
                raise ObjectDoesNotExist("company info not found")

            # print("company",company_info_obj)
            company = Company.objects.get(id=company_info_obj.company_id.id)
            if not company:
                raise ObjectDoesNotExist("company not found")
            
            # print("company from company obj", company)
            # print("watchlist",watchlist_obj)
            watchlist_obj.company.remove(company)
            watchlist_obj.save()
            
            return watchlist_obj
            
        except Exception as err:
            # print(tb.print_tb(err.__traceback__))
            raise serializers.APIException({
                "error": str(err),
                "name": err.__class__.__name__
            })
