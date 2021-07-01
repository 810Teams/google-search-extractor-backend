"""
    Extractor application views
    extractor/views.py
"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response

from core.util.filters import filter_queryset, filter_queryset_permission
from extractor.models import ScrapeResult, ScrapeResultPage, ScrapeResultItem
from extractor.permissions import IsScrapeResultOwner
from extractor.serializers import NotExistingScrapeResultSerializer, ExistingScrapeResultSerializer
from extractor.serializers import ScrapeResultPageSerializer, ScrapeResultItemSerializer


class ScrapeResultViewSet(viewsets.ModelViewSet):
    """ Scrape result view set """
    queryset = ScrapeResult.objects.all()
    http_method_names = ('get', 'post', 'delete', 'head', 'options')

    def get_permissions(self):
        """ Get permissions """
        if self.request.method in ('GET', 'DELETE'):
            return (permissions.IsAuthenticated(), IsScrapeResultOwner())
        elif self.request.method == 'POST':
            return (permissions.IsAuthenticated(),)
        return tuple()

    def get_serializer_class(self):
        """ Get serializer class """
        if self.request.method == 'POST':
            return NotExistingScrapeResultSerializer
        return ExistingScrapeResultSerializer

    def list(self, request, *args, **kwargs):
        """ List instances """
        queryset = self.filter_queryset(self.get_queryset())
        queryset = filter_queryset_permission(queryset, request, self.get_permissions())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class ScrapeResultPageViewSet(viewsets.ModelViewSet):
    """ Scrape result page view set """
    queryset = ScrapeResultPage.objects.all()
    http_method_names = ('get', 'head', 'options')
    serializer_class = ScrapeResultPageSerializer

    def get_permissions(self):
        """ Get permissions """
        if self.request.method == 'GET':
            return (permissions.IsAuthenticated(), IsScrapeResultOwner())
        return tuple()

    def list(self, request, *args, **kwargs):
        """ List instances """
        queryset = self.filter_queryset(self.get_queryset())
        queryset = filter_queryset_permission(queryset, request, self.get_permissions())
        queryset = filter_queryset(queryset, request, target_param='scrape_result', is_foreign_key=True)
        queryset = filter_queryset(queryset, request, target_param='keyword', is_foreign_key=False)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class ScrapeResultItemViewSet(viewsets.ModelViewSet):
    """ Scrape result item view set """
    queryset = ScrapeResultItem.objects.all()
    http_method_names = ('get', 'head', 'options')
    serializer_class = ScrapeResultItemSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'url', 'text')

    def get_permissions(self):
        """ Get permissions """
        if self.request.method == 'GET':
            return (permissions.IsAuthenticated(), IsScrapeResultOwner())
        return tuple()

    def list(self, request, *args, **kwargs):
        """ List instances """
        queryset = self.filter_queryset(self.get_queryset())
        queryset = filter_queryset_permission(queryset, request, self.get_permissions())
        queryset = filter_queryset(queryset, request, target_param='scrape_result_page', is_foreign_key=True)
        queryset = filter_queryset(queryset, request, target_param='is_adwords', is_foreign_key=False)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
