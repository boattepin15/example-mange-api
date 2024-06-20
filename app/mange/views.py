from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from mange.serializers import MangeSerializer, MangeImageserializer, EpisodeSerializer
from core.models import Mange, Episode
from mange.permissions import PublicReadOnly

class MangeViewSet(viewsets.ModelViewSet):
    """ Viewset สำหรับ Mange """
    serializer_class = MangeSerializer
    queryset = Mange.objects.all()
    permission_classes = [IsAuthenticated | PublicReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        ''' ส่ง serializer class กลับไปหา request '''
        if self.action == 'list' or self.action == 'retrieve':
            return MangeSerializer
        elif self.action == 'upload_image':
            return MangeImageserializer
        return self.serializer_class

    @action(detail=True, methods=['post'], url_path='upload-image', permission_classes=[IsAuthenticated], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        mange = self.get_object()
        serializer = self.get_serializer(mange, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EpisodeViewset(viewsets.ModelViewSet):
    """ สร้าง Viewset CRUD """
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all()
    permission_classes = [IsAuthenticated | PublicReadOnly]
    
