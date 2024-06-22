from django.urls import (
    path,
    include,
)
from mange import views
from rest_framework.routers import DefaultRouter
app_name = 'mange'

router = DefaultRouter()
router.register('mange', views.MangeViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('episodes/create', views.CreateEpisodeViewset.as_view(),name='episode-create'),
    path('episodes/list', views.ListEpisodesViewset.as_view(), name='episodes-list')
]

