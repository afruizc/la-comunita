from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from core import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, 'user')
router.register(r'communities', views.CommunityViewSet, 'community')
router.register(r'groups', views.GroupViewSet, 'group')
router.register(r'chats', views.ChatViewSet, 'chat')
router.register(r'messages', views.MessageViewSet, 'message')
router.register(r'groupinvitations', views.GroupInvitationViewSet,
                'groupinvitation')
router.register(r'chatinvitations', views.ChatInvitationViewSet,
                'chatinvitation')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^get-auth-token/', obtain_auth_token)
]
