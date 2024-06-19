from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _

class UserSerializer(serializers.ModelSerializer):
    """สร้าง Serializer สำหรับ User Model"""

    #กำหนดคุณสมบัติ
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        
        #กำนหมด field password สามารถเขียนได้อย่างเดียว ไม่สามารถดูได้
        #และมีความยาวอย่างน้อย 5 ตัวหนักสือ
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }


    def create(self, validated_data):
        """สร้าง User และเข้ารหัสผ่าน"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ อัพเดท User"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
