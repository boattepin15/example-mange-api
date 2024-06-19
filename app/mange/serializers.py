from rest_framework import serializers
from core.models import Mange


class MangeSerializer(serializers.ModelSerializer):
    """ สร้าง Serializer สำหรับ Mange Model"""
    class Meta:
        model = Mange
        #ส่งทุก fields กลับไปหา client
        fields = '__all__'
        #กำนหดให้ id สามารถอ่านได้อย่างเดียว
        read_only_fields = ['id']
        

