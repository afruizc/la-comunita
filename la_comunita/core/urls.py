from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from core import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'communities', views.CommunityViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token-auth/', obtain_auth_token)
]
