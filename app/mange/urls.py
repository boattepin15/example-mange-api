from django.urls import (
    path,
    include,
)
from mange import views
from rest_framework.routers import DefaultRouter
app_name = 'mange'

router = DefaultRouter()
router.register('mange', views.ManageViewSet)
urlpatterns = [
    path('', include(router.urls)),
]