"""
    Extractor Application URLs
    extractor/urls.py
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from extractor.views import ScrapeResultViewSet


router = DefaultRouter()
router.register('scrape-result', ScrapeResultViewSet)

urlpatterns = [
    path('', include(router.urls))
]
