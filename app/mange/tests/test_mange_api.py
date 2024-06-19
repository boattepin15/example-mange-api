from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
import json
from django.contrib.auth import get_user_model
from mange.serializers import (
    MangeSerializer
)
from core.models import Mange

MANGE_URL = reverse('mange:mange-list')

def user_admin():
    return get_user_model().objects.create_superuser(
        email='email@test.com',
        username='username',
        password='password1234'
    )

def user():
    return get_user_model().objects.create_user(
        email='email@test.com',
        username='username',
        password='password1234'
    )
    

def mange_create_admin():
 
    payload = {
        'title':'title',
        'profile':'',
        'author_by':'author_by',
        'draw_by':'draw_by',
        'upload_by':user_admin()
    }
    mange = Mange.objects.create(**payload)
    return mange


class PublicMangeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_retrieve_list_all(self):
        """ ทดสอบดึงข้อมูลขึ้นมา โดยผู้ใช้งานทั่วไป"""
        mange_create_admin()
        manges = Mange.objects.all()
        serializer = MangeSerializer(manges, many=True)
        res = self.client.get(MANGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(json.dumps(res.data), json.dumps(serializer.data))

    def test_create_forbidden(self):
        """ ทดสอบให้ ผู้ใช้งานที่ไม่ใช่ is_superuser หรือ admin สร้าง มังงะ"""

        payload = {
            'title':'title',
            'profile':'',
            'author_by':'author_by',
            'draw_by':'draw_by',
            'upload_by':user()
        }
        
        res = self.client.post(MANGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_forbidden(self):
        """ ทดสอบอัพเดต Patch โดยผู้ใช้งานทั่วไป """
        payload = {
            'title':'title',
            'profile':'',
            'author_by':'author_by',
            'draw_by':'draw_by',
            'upload_by':user_admin()
        }
        Mange.objects.create(
           **payload
        )
        res = self.client.patch(MANGE_URL, {'title':payload['title']})
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_put_forbidden(self):
        """ ทดสอบอัพเดตโดยใช้ put method """
        payload = {
            'title':'title',
            'profile':'',
            'author_by':'author_by',
            'draw_by':'draw_by',
            'upload_by':user_admin()
        }
        Mange.objects.create(
           **payload
        )
        res = self.client.put(MANGE_URL, title = payload['title'])
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_forbidden(self):
        """ ทดสอบลบข้อมูลโดยผู้ใช้งานทั่วไป """
        payload = {
            'title':'title',
            'profile':'',
            'author_by':'author_by',
            'draw_by':'draw_by',
            'upload_by':user_admin()
        }
        mange = Mange.objects.create(
           **payload
        )
        res = self.client.delete(MANGE_URL, id = mange.id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    

class PrivateMangeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = user_admin()
        self.client.force_authenticate(self.user)
    
    def test_create_mange_admin(self):
        """ ทดสอบให้ แอดมินสร้าง Mnage """
        payload = {
            'title':'title',
            'profile':'',
            'author_by':'author_by',
            'draw_by':'draw_by',
            'upload_by':self.user.id
        }
        
        res = self.client.post(MANGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)