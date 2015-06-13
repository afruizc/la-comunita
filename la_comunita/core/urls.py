from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'communities', views.CommunityViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
