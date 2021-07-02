"""
    Extractor Application URLs
    extractor/urls.py
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from extractor.views import ScrapeResultViewSet, ScrapeResultPageViewSet, ScrapeResultItemViewSet


router = DefaultRouter()
router.register('scrape-result/page', ScrapeResultPageViewSet)
router.register('scrape-result/item', ScrapeResultItemViewSet)
router.register('scrape-result', ScrapeResultViewSet)

urlpatterns = [
    path('', include(router.urls))
]
