from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import path, reverse, include, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from .models import UserAccount

from .serializers import UserProfileDetailSerializer
from faker import Faker
from rest_framework import status


# Create your tests here.

class AccountTest(APITestCase):
    fixtures = ['user.json']

    def test_register(self):
        _response = self.client.post('/auth/register/', format="json")
        _data = _response.json()
        print("Registration  Response : ",_data)
        self.assertEqual(_response.status_code, 200)

    def test_login(self):
        _data = {
            "username":'aa',
            "password": "1234",
        }
        _response = self.client.post('/auth/login/', data=_data, format="json")
        _data = _response.json()
        print("Login Response : ",_data)
        self.assertEqual(_response.status_code, 200)

    def test_get_user(self):
        _response = self.client.get('/auth/user/', format="json")
        _data = _response.json()
        print(_data)
        self.assertEqual(_response.status_code, 401)

    def test_post_profile_update(self):
        _response = self.client.get('/auth/profile_update/1/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 405)
