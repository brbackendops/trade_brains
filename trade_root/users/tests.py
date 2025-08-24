from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework import status

from .models import User

# Create your tests here.

class UserAccountTests(TestCase):
    
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'test@hotmail.com', 'one' , 'two' , 'password'
        )
        
        self.assertEqual(super_user.email, "test@hotmail.com")
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email=None,first_name=None,last_name=None,password=None
            )
        
        
    def test_new_user(self):
        db = get_user_model()
        new_user = db.objects.create_user(
            'test@hotmail.com', 'one' , 'two' , 'password'
        )
        
        self.assertEqual(new_user.email, "test@hotmail.com")
        self.assertIsNotNone(new_user.password)
        self.assertFalse(new_user.is_superuser)
        self.assertFalse(new_user.is_staff)
        self.assertTrue(new_user.is_active)
        
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='',first_name='',last_name='',password=''
            )
        
class UserAccountApiTests(APITestCase):
    
    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'password'
        
        self.user_model = get_user_model()
        self.User = self.user_model.objects.create_user(email=self.email,password=self.password,first_name='t',last_name='est')
        
    
    def test_user_creation_api(self):
        url = reverse('register-user')
        
        data = {
            "first_name": "test",
            "last_name": "123",
            "designation": "test",
            "email": "test1@mail.com",
            "password": "test1234"
        }
        
        response = self.client.post(url,data,format='json')

        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_creation_fail_api(self):
        url = reverse('register-user')
        
        data = {
            "first_name": "test",
            "last_name": "123",
            "designation": "test",
            "email": "",
            "password": "test1234"
        }
        
        response = self.client.post(url,data,format='json')

        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_login(self):
        
        url = reverse('login-token')
        
        response = self.client.post(url,{ 'email': self.email, 'password': self.password },format='json')        
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertIn('access_token',response.data)
        self.assertIn('refresh',response.data)