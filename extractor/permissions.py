"""
    Extractor Application Permissions
    extractor/permissions.py
"""

from rest_framework import permissions

from extractor.models import ScrapeResult, ScrapeResultPage, ScrapeResultItem


class IsScrapeResultOwner(permissions.BasePermission):
    """ Scrape result owner permission """
    def has_object_permission(self, request, view, obj):
        """ Check object permission """
        if isinstance(obj, ScrapeResultItem):
            obj = ScrapeResultPage.objects.get(pk=obj.scrape_result_page.id)
        if isinstance(obj, ScrapeResultPage):
            obj = ScrapeResult.objects.get(pk=obj.scrape_result.id)

        if isinstance(obj, ScrapeResult):
            return request.user.is_authenticated and obj.user is not None and request.user.id == obj.user.id

        return False
