"""
    Extractor Application Permissions
    extractor/permissions.py
"""

from rest_framework import permissions

from extractor.models import ScrapeResult


class IsScrapeResultOwner(permissions.BasePermission):
    """ Scrape result owner permission """
    def has_object_permission(self, request, view, obj):
        """ Check object permission """
        if isinstance(obj, ScrapeResult):
            return request.user.is_authenticated and obj.user is not None and request.user.id == obj.user.id
        return False
