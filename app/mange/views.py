from mange.serializers import MangeSerializer
from core.models import Mange
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from mange.permissions import PublicReadOnly



class ManageViewSet(viewsets.ModelViewSet):
    """ Viewset สำหรับ MangeSerializer """
    serializer_class = MangeSerializer
    queryset = Mange.objects.all()
    permission_classes = [IsAuthenticated | PublicReadOnly]