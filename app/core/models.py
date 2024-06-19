from django.db import models
import uuid
import os
from unittest.mock import patch
from django.contrib.auth.models import (
    AbstractBaseUser,  
    BaseUserManager,
    PermissionsMixin
)
from django.conf import settings

from django.contrib.auth.models import BaseUserManager

def mange_image_file_path(instance, filename):
    """ สร้าง path สำหรับ mange profile"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'mange', filename)



class UserManager(BaseUserManager):
    """ สร้างระบบ จัดการผู้ใช้งานและผู้ดูแล"""
    
    def create_user(self, email, username, password=None, **extra_fields):
        """ สร้างระบบสมัครสมาชิกสำหรับผู้ใช้งานทั่วไป"""

        if not email:
            # ตรวจสอบว่ามีการใส่ Email หรือเปล่า
            raise ValueError('โปรดกรอก Email เพื่อสมัครสมาชิก')

        if not username:
            raise ValueError('โปรดกำหนด Username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # เมื่อเชิฟ ผู้ใช้งานใหม่เสร็จ ก็จะส่ง user 
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        """ สร้างระบบสมัครสมาชิกแอดมิน"""
        # เปลี่ยนให้ fields is_staff = True และ is_superuser = True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # ตรวจสอบว่า User ที่สมัครเข้ามาเป็น แอดมินอยู่แล้วไหม
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser ต้องมี is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser ต้องมี is_superuser=True')

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """ สร้าง User model Custom จาก AbstractBaseUser"""
    #กำหนด Feild สำหรับ models
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 

    objects = UserManager()
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Mange(models.Model):
    """สร้าง Models มังงะ (Mange)"""
    title = models.CharField(max_length=255)
    profile = models.ImageField(null=True, upload_to=mange_image_file_path)
    author_by = models.CharField(max_length=255)
    draw_by = models.CharField(max_length=255)
    upload_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE 
    )

    def __str__(self):
        return self.title
 
    


    
