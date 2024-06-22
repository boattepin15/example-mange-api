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
    ''' สร้าง serializer สำหรับ ep หรือ ตอนสำหรับมังงะ '''
    mange_id = serializers.PrimaryKeyRelatedField(queryset=Mange.objects.all(), source='mange', write_only=True)
    mange = MangeSerializer(read_only=True)

    class Meta:
        model = Episode
        fields = ['id', 'mange', 'mange_id', 'ep', 'content']
        read_only_fields = ['id']

    def validate_ep(self, value):
        """ตรวจสอบค่า ep"""
        if value <= 0:
            raise serializers.ValidationError('หมายเลขตอนต้องมากกว่าศูนย์')
        return value

    def validate(self, data):
        """ตรวจสอบข้อมูลทั้งหมด"""
        if 'mange' not in data:
            raise serializers.ValidationError('ต้องระบุข้อมูลมังงะ')
        return data

    def create(self, validated_data):
        mange = validated_data.pop('mange')
        episode = Episode.objects.create(mange=mange, **validated_data)
        return episode