from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Mange, Episode
from core import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from unittest.mock import patch
import os



class Tests_Model(TestCase):
    """ Class สำหรับ TestCase Models"""

    def test_create_user_success(self):
        """ ทดสอบ Model User และทดสอบการสร้าง ผู้ใช้งานหรือฟังก์ชัน create_user"""
        playload = {
            'email':'email@test.com',
            'username':'username',
            'password':'password1234'
        }
        #สร้าง User จาก ฟังก์ชัน get_user_model
        user = get_user_model().objects.create_user(
                email=playload['email'],
                username=playload['username'],
                password=playload['password']
            )
        
        self.assertEqual(user.email, playload['email'])
        self.assertEqual(user.username, playload['username'])
        self.assertTrue(user.check_password(playload['password']))
    
        
    def test_create_user_undefine_username(self):
        """ ทดสอบ function create_user ว่าได้กำหนด username มาหรือไม่"""
        playload = {
            "email": 'email@test.com',
            'password': 'password1234'
        }
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_user(
                email=playload['email'],
                password=playload['password'],
                username=''
            )
        self.assertEqual(str(context.exception), 'โปรดกำหนด Username')
    


    def test_create_superuser_undefine_username(self):
        """ทดสอบการสร้าง superuser โดยไม่กำหนด username"""
        playload = {
            'email':'email@test.com',
            'password':'password1234',
            'username':''
        }
   
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_superuser(
                email=playload['email'],
                password=playload['password'],
                username=playload['username']
            )
        self.assertEqual(str(context.exception), "โปรดกำหนด Username")


    def test_create_superuser_success(self):
        """ ทดสอบ ฟังก์ชัน create_superuser สมัครแอดมิน"""
        playload = {
            'email':'email@test.com',
            'username':'admin',
            'password':'password1234'
        }

        superuser = get_user_model().objects.create_superuser(
            email=playload['email'],
            username=playload['username'],
            password=playload['password']
        )
        self.assertEqual(str(superuser), playload['username'])
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


    def test_create_superuser_without_is_staff_raises_error(self):
        """ทดสอบการสร้าง superuser โดยไม่มี is_staff จะ raise error"""
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_superuser(
                email='superuser@test.com',
                password='superuserpass',
                username='namesuperuser',
                is_staff=False
            )
        self.assertEqual(str(context.exception), 'Superuser ต้องมี is_staff=True')



    def test_create_superuser_without_is_superuser_raises_error(self):
        """ทดสอบการสร้าง superuser โดยไม่มี is_superuser จะ raise error"""
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_superuser(
                email='superuser@test.com',
                password='superuserpass',
                username='namesuperuser',
                is_superuser=False
            )
        self.assertEqual(str(context.exception), 'Superuser ต้องมี is_superuser=True')
    
    def test_create_mange(self):
        """ ทดสอบสร้าง model mange"""
        user = get_user_model().objects.create_user(
            email='email@test.com',
            username='username',
            password='password1234'
        )
        payload = {
            'title':'test title',
            'profile':'',
            'author_by':'test author_by',
            'draw_by':'test draw_by',
            'upload_by':user
        }
        mange = Mange.objects.create(
            **payload
        )
        self.assertEqual(str(mange), payload['title'])
        self.assertEqual(mange.title, payload['title'])
        self.assertEqual(mange.author_by, payload['author_by'])
        self.assertEqual(mange.draw_by, payload['draw_by'])
        self.assertEqual(mange.upload_by, payload['upload_by'])

    @patch('core.models.uuid.uuid4')
    def test_mange_file_name_uuid(self, mock_uuid):
        """ ทดสอบ image Patch"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.mange_image_file_path(None, 'test.jpg')
        
        self.assertEqual(file_path, f'uploads/mange/{uuid}.jpg')
    
    def test_create_episodes(self):
        """ทดสอบสร้างตอน หรือ episodes ให้กับ mange"""
        user = get_user_model().objects.create_user(
            email='email@test.com',
            username='username',
            password='password1234'
        )
        mange = Mange.objects.create(
            title='ชื่อมังงะ',
            profile=None,  
            author_by='ผู้เขียน',
            draw_by='ผู้วาด',
            upload_by=user  
        )

        # ตอนนี้สร้าง Episode
        episode = Episode.objects.create(
            ep=1,  
            content='เนื้อหา',
            mange=mange
        )
        self.assertEqual(str(mange), 'ชื่อมังงะ')        
        self.assertEqual(episode.ep, 1)
        self.assertEqual(str(episode), '1')
