
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse


from .models import WatchList
from ..company.models import Company , CompanyInfo

# rest_framework
from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework import status


# Create your tests here.

class WatchListTestCase(TestCase):
    
    def setUp(self):
        self.user_model = get_user_model()
        self.name = "test-list"
        self.User = self.user_model.objects.create(email='test@mail.com',password='test123')
        self.watchlist = WatchList.objects.create(
            user=self.User,
            name=self.name
        )
        
        self.company = Company.objects.create(companyy_name='test-company')
    
    def test_new_watchlist(self):
        watchlist = WatchList.objects.create(
            user=self.User,
            name=self.name
        )
        
        self.assertEqual(watchlist.user.id, self.User.id)
        self.assertEqual(watchlist.name,self.name)
        
        with self.assertRaises(IntegrityError):
            watchlist = WatchList.objects.create(
                user=self.User,
                name=None
            )

    def test_watchlist_add(self):
        
        company_1 = Company.objects.create(companyy_name='test-company')
        company_2 = Company.objects.create(companyy_name='test-company')
                        
        self.watchlist.company.set([company_1,company_2])
        self.watchlist.save()        
        
        self.assertEqual(self.watchlist.company.count(), 2)
        
        company_3 = company_2 = Company.objects.create(companyy_name='test-company')
        self.watchlist.company.add(company_3)
        self.watchlist.save()
        
        self.assertEqual(self.watchlist.company.count(), 3)
        
        
    def test_watchlist_remove(self):
        
        company_1 = Company.objects.create(companyy_name='test-company')
        company_2 = Company.objects.create(companyy_name='test-company')
                        
        self.watchlist.company.set([company_1,company_2])
        self.watchlist.save()        
        
        self.watchlist.company.remove(company_2)
        self.watchlist.save()
        
        self.assertEqual(self.watchlist.company.count(), 1)


class WatchListApiTestCase(APITestCase):
    
    def setUp(self):
        
        self.email='test@mail.com'
        self.password='test123'
        
        self.user_model = get_user_model()
        self.User = self.user_model.objects.create_user(email=self.email,password=self.password,first_name='test',last_name='1')
        
        self.watchlist = WatchList.objects.create(name='test-sample',user=self.User)
        
        self.login_url = reverse('login-token')
        
    
    
    def test_permission_on_watchlist_list_view(self):
        url = reverse('list-watchlist')    
        
        response = self.client.get(url)
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_watchlist_list_api(self):
        
        
        response = self.client.post(self.login_url,{ 'email': self.email, 'password': self.password },format='json')        
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertIn('access_token',response.data)
        self.assertIn('refresh',response.data)
                
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data['access_token'])
        
        
        w1 = WatchList.objects.create(name='test1',user=self.User)
        w2 = WatchList.objects.create(name='test2',user=self.User)
        w3 = WatchList.objects.create(name='test3',user=self.User)
                    
        url = reverse('list-watchlist')        
        
        response = self.client.get(url)        
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['data']),0)
        
    def test_watchlist_create_api(self):
        
        
        response = self.client.post(self.login_url,{ 'email': self.email, 'password': self.password },format='json')        
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertIn('access_token',response.data)
        self.assertIn('refresh',response.data)
                
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data['access_token'])        
        
        
        data = {
            'name': 'test1'
        }
        
        url = reverse('create-watchlist')
        
        response = self.client.post(url,data,format="json")
        
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_can_add_to_watchlist(self):
        
        
        response = self.client.post(self.login_url,{ 'email': self.email, 'password': self.password },format='json')        
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertIn('access_token',response.data)
        self.assertIn('refresh',response.data)
                
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data['access_token'])        
        
        
        company_1 = Company.objects.create(companyy_name='test-company')
        company_info_1 = CompanyInfo.objects.create(company_id=company_1,symbol='test1',scrip_code="t001")
        company_2 = Company.objects.create(companyy_name='test-company')
        company_info_2 = CompanyInfo.objects.create(company_id=company_2,symbol='test2',scrip_code="t002")
        
        data = {
            'company_code': 't001'
        }
        
        url = reverse('add-to-watchlist',args=[self.watchlist.id])
        
        response = self.client.post(url,data,format="json")
        
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        


    def test_can_remove_from_watchlist(self):
        
        
        response = self.client.post(self.login_url,{ 'email': self.email, 'password': self.password },format='json')        
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertIn('access_token',response.data)
        self.assertIn('refresh',response.data)
                
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data['access_token'])        
        
        
        company_1 = Company.objects.create(companyy_name='test-company')
        company_info_1 = CompanyInfo.objects.create(company_id=company_1,symbol='test1',scrip_code="t001")
        company_2 = Company.objects.create(companyy_name='test-company')
        company_info_2 = CompanyInfo.objects.create(company_id=company_2,symbol='test2',scrip_code="t002")
        
        data = {
            'company_code': 't001'
        }
        
        url = reverse('remove-from-watchlist',args=[self.watchlist.id])
        
        response = self.client.post(url,data,format="json")
        
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)