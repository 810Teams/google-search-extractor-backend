"""
    User Application URLs
    user/urls.py
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import LoginAPIView, UserViewSet, MyUserView


router = DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    path('user/me/', MyUserView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('', include(router.urls))
]
