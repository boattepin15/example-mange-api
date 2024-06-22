from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer, AuthTokenSerializers
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken  


class CreateuserView(generics.CreateAPIView):
    """ Viewset สำหรับ สมัครสมาชิกใหม่"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """สร้าง token ของ user"""
    serializer_class = AuthTokenSerializers
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES  

class ManagerUserView(generics.RetrieveUpdateAPIView):
    """ระบบจัดการ Authentication สำหรับ User"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes  = [permissions.IsAuthenticated]
    
    def get_object(self):
        """เมื่อผ่านการ authenticated ก็จะส่ง user กลับมา"""
        return self.request.user

