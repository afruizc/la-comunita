from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'communities', views.CommunityViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'private_chats', views.PrivateChatViewSet)
router.register(r'group_chats', views.GroupChatViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
