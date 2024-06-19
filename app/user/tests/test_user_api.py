from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status




#กำนหด Url สมัครสมาชิก user/create
CREATE_USER_URL = reverse('user:create')
#กำหนด url สร้าง token user/token
TOKEN_USER = reverse('user:token')

#กำหนด url profile user/profile
PROFILE_USER = reverse('user:profile')



class PublicUserApiTests(TestCase):
    """ สร้าง Test API ของ User แบบ Public"""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """ทดสอบ API สมัคร สมาชิก"""
        payload = {
            "email":'email@test.com',
            'username':'username',
            'password':'password1234'
        }
        #ทดสอบ request ไปยัง API method post -> /api/user/create 
        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(username=payload['username'])
        #ทดสอบว่าสมัครสมาชิกใหม่ได้
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        #ทดสอบว่าการเข้ารหัสถูกต้อง
        self.assertTrue(user.check_password(payload['password']))
        #ทดสอบว่าจะไม่มีการส่ง password กลับมาผ่าน respone
        self.assertNotIn('password', res.data)
    
    def test_user_with_email_exists_error(self):
        """ทดสอบ ขั้นตอนสมัคร เช็คว่ามีผู้ใช้งานที่เราสมัครไปแล้ว"""
        payload = {
            "email":'email@test.com',
            'username':'username',
            'password':'password1234'
        }
        get_user_model().objects.create_user(
            email=payload['email'],
            username=payload['username'],
            password=payload['password']
        )
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_shrot_error(self):
        """ทดสอบว่า password มีความยาวน้อยกว่ากำหนดหรือไม่"""
        payload = {
            "email":'email@test.com',
            'username':'username',
            'password':'pass'
        }
        res = self.client.post(CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_token_for_user(self):
        """ ทดสอบสร้าง token สำหรับ valid credentials """
        user_details = {
            "email": 'test@gmail.com',
            "username": 'Test Name',
            "password": 'test-user-password12345'
        }
        user = get_user_model().objects.create_user(
            email=user_details['email'],
            username=user_details['username'],
            password=user_details['password']
            
        )
        payload = {
            'username': user_details['username'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_USER, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_bad_credentials(self):
        """ทดสอบ สร้าง token เพื่อขอ credentials ไม่สำเสร็จ"""

        get_user_model().objects.create_user(
            email='email@test.com',
            username='username',
            password='password1234'
        )
        #สร้าง payload ให้รหัสผ่านผิด
        payload = {
            'username':'username',
            'password':'password4321'         
        }
        
        res = self.client.post(TOKEN_USER, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_blank_password(self):
        """ ทดสอบสร้าง password error โดยไม่ใส่ password """
        payload = {
            'username':'username',
            'password':''
        }
        res = self.client.post(TOKEN_USER, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
    
    def test_return_user_unauthorized(self):
        '''ทดสอบ ให้ขอเข้าใช้งานไม่ผ่าน authenticated'''
        res = self.client.get(PROFILE_USER)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PraivateUserApiTests(TestCase):
    """ ทดสอบ API request ผ่าน authentication"""

    def setUp(self):
        #กำหนดผู้ใช้งานที่ผ่าน authentication
        self.user = get_user_model().objects.create_user(
            email='email@test.com',
            username='username',
            password='password1234'
        )
        #ใช้สำหรับขอ request 
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrive_profile_success(self):
        '''ทดสอบ ขอ Profile สำหรับ user'''
        res = self.client.get(PROFILE_USER)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email':self.user.email,
            'username':self.user.username
        })
    def test_post_profile_not_allowed(self):
        """ ทดสอบ post medthod for profile API"""
        res = self.client.post(PROFILE_USER, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)        

    def test_update_profile(self):
        """ทดสอบ อัพเดต profile สำรหับ authenticated ของ user """
        payload = {
            'username':'update username',
            'password':'update password'
        }
        self.user.refresh_from_db()
        res = self.client.patch(PROFILE_USER, payload)
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        