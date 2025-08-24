from rest_framework import serializers
from .models import Company , CompanyInfo



class CompanyInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyInfo
        exclude = ['company_id']
    
class CompanyRetrieveSerializer(serializers.ModelSerializer):
    company_info = CompanyInfoSerializer(read_only=True)
    class Meta:
        model = Company
        fields = ['companyy_name','company_info']


class CompanyCreationSerilalizer(serializers.ModelSerializer):
    
    symbol = serializers.CharField(write_only=True,allow_null=True)
    scrip_code = serializers.CharField(write_only=True,allow_null=True)
    
    company_name = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Company
        fields = ['company_name','symbol','scrip_code']
    
    
    
    def create(self,validated_data):
        if validated_data.get('symbol') and validated_data.get('scrip_code'):
            try:
                company = Company.objects.create(companyy_name=validated_data.get('company_name'))
                if company:
                    data = {
                        "company_id": company,
                        "symbol": validated_data.get('symbol'),
                        "scrip_code": validated_data.get('scrip_code')
                    }
            
                    CompanyInfo.objects.create(**data)
                    return company
            except Exception as err:
                raise serializers.APIException({
                    "error": str(err),
                    "name": err.__class__.__name__
                })
        
        return Company.objects.create(companyy_name=validated_data.get("company_name"))

class CompanyInfoUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyInfo
        exclude = ['__all__']