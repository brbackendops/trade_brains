from django.test import TestCase
from django.db.models import QuerySet
from .models import Company , CompanyInfo
from django.db import IntegrityError
from django.urls import reverse


from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework import status


# Create your tests here.

class CompanyTestCase(TestCase):
    
    def setUp(self):
        self.company_name = 'test'
        self.price = 10.00
        self.company_test = Company.objects.create(
            companyy_name="test",
            price=10.00
        )
        self.company_pk = self.company_test.id
    
    
    def test_company_create(self):
        company = Company.objects.create(
            companyy_name=self.company_name,
            price = self.price
        )
        
        self.assertEqual(company.companyy_name,self.company_name)
        self.assertEqual(company.price,self.price)
        
        with self.assertRaises(IntegrityError):
            Company.objects.create(companyy_name=None)

    
    def test_company_get(self):
        company = Company.objects.get(pk=self.company_pk)
        
        self.assertEqual(company.companyy_name,self.company_name)
        self.assertEqual(company.price,self.price)
        
        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(pk=100)

    def test_company_list(self):
        company = Company.objects.all()
        
        self.assertGreater(len(company),0)
        self.assertIsInstance(company,QuerySet)
        
class CompanyInfoTestCase(TestCase):
    def setUp(self):
        
        self.company_name = 'test'
        self.price = 10.00
        self.company = Company.objects.create(
            companyy_name=self.company_name,
            price = self.price
        )         
        
        self.scrip_code = 'T2123T'
        self.symbol = "TTT"
        self.company_info_test = CompanyInfo.objects.create(
            company_id=self.company,
            symbol=self.symbol,
            scrip_code=self.scrip_code
        )
        self.info_pk = self.company_info_test.id
               
    
    
    def test_companyinfo_create(self):
        
        company = Company.objects.create(
            companyy_name=self.company_name,
            price = self.price
        )        
        
        company_info = CompanyInfo.objects.create(
            company_id=company,
            symbol=self.symbol,
            scrip_code = self.scrip_code
        )
        
        self.assertEqual(company_info.company_id.id,company.id)
        self.assertEqual(company_info.symbol,self.symbol)
        self.assertEqual(company_info.scrip_code,self.scrip_code)
        
        with self.assertRaises(IntegrityError):
            company_info = CompanyInfo.objects.create(
                company_id=self.company,
                symbol=self.company_name,
                scrip_code = self.price
            )
        

    
    def test_companyinfo_get(self):
        company_info = CompanyInfo.objects.get(pk=self.info_pk)
        
        self.assertEqual(company_info.symbol,self.symbol)
        self.assertEqual(company_info.scrip_code,self.scrip_code)
        
        with self.assertRaises(CompanyInfo.DoesNotExist):
            CompanyInfo.objects.get(pk=100)

    def test_companyinfo_list(self):
        company_infos = CompanyInfo.objects.all()
        
        self.assertGreater(len(company_infos),0)
        self.assertIsInstance(company_infos,QuerySet)

class CompanyApiTests(APITestCase):
    
    def test_company_creation_api(self):
        url = reverse('create-company')
        
        data = {
            "company_name": "test123",   
            "scrip_code": None,
            "symbol": None                     
        }
        
        response = self.client.post(url,data,format='json')
        # print(response.data)
        # print(response.status_code)
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(),1)
        self.assertEqual(Company.objects.get().companyy_name,data["company_name"])
        
    def test_company_list_api(self):
        
        Company.objects.create(companyy_name='test1')
        Company.objects.create(companyy_name='test2')
        Company.objects.create(companyy_name='test3')
        
        url = reverse('list-companies')
                
        response = self.client.get(url)
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(Company.objects.count(),0)