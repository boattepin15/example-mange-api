from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
import json
from django.contrib.auth import get_user_model
from mange.serializers import (
    MangeSerializer,
    EpisodeSerializer
)
from core.models import Mange, Episode

MANGE_URL = reverse('mange:mange-list')
#EPISODES_URL = reverse('mange:episode-list')
EPISODE_CREATE_URL = reverse('mange:episode-create')
EPISODES_LIST_URL = reverse('mange:episodes-list')

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
            'upload_by':self.user.id,
        }
        res = self.client.post(MANGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    def test_create_mange_episodes(self):
        """ ทดสอบสร้าง Episode ของ Mnage"""
        payload = {
            'title':'title',
            'profile':'',
            'author_by':'author_by',
            'draw_by':'draw_by',
            'upload_by':self.user,
            }
        mange = Mange.objects.create(**payload)
        episodes = Episode.objects.create(
            mange_id=mange.id,
            ep = 1,
            content = "Test Content"
        )
        serializer = EpisodeSerializer(episodes)
        res = self.client.post(EPISODE_CREATE_URL, {
            'mange_id': mange.id,
            'ep': 1,
            'content': 'Test Content'
        })
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data['mange'], res.data['mange'])
        self.assertEqual(serializer.data['ep'], res.data['ep'])
        self.assertEqual(serializer.data['content'], res.data['content'])
    
def test_list_mange_episodes(self):
        """ทดสอบดึงข้อมูลทั้งหมด Episode Model"""
        payload = {
            'title': 'title',
            'profile': '',
            'author_by': 'author_by',
            'draw_by': 'draw_by',
            'upload_by': self.user,  
        }
        mange = Mange.objects.create(**payload)
        Episode.objects.create(
            mange_id=mange.id,
            ep=1,
            content="Test Content 1"
        )
        Episode.objects.create(
            mange_id=mange.id,
            ep=2,
            content="Test Content 2"
        )
        episodes = Episode.objects.all()
        serializer = EpisodeSerializer(episodes, many=True)
        res = self.client.get(EPISODES_LIST_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(json.dumps(res.data)), serializer.data)