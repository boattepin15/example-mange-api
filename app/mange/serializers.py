from rest_framework import serializers
from core.models import Mange, Episode





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

class EpisodeSerializer(serializers.ModelSerializer):
    ''' สร้าง serializer สำหรับ ep หรือ ตอนสำหรับมังงะ'''
    
    # ใช้ PrimaryKeyRelatedField เพื่อให้แสดงเฉพาะ ID ของ Mange
    #mange = serializers.PrimaryKeyRelatedField(queryset=Mange.objects.all())

    # แสดง Json ของ Model Mange ด้วย MangeSerializer
    mange = MangeSerializer(read_only=True)
    class Meta:
        model = Episode
        fields = ['mange', 'ep','content']
        read_only_fields = ['id']
