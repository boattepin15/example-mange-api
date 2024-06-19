from rest_framework import serializers
from core.models import Mange

class MangeSerializer(serializers.ModelSerializer):
    """ สร้าง Serializer สำหรับ Mange Model"""
    class Meta:
        model = Mange
        fields = '__all__'
        read_only_fields = ['id']

class MangeImageserializer(serializers.ModelSerializer):
    ''' Serializer สำหรับ upload รูป profile mange'''
    class Meta:
        model = Mange
        fields = ['id', 'profile']
        read_only_fields = ['id']
        extra_kwargs = {
            'profile': {'required': True}
        }
