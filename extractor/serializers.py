"""
    Extractor Application Serializers
    extractor/serializers.py
"""

from rest_framework import serializers

from extractor.models import ScrapeResult, ScrapeResultPage, ScrapeResultItem


class NotExistingScrapeResultSerializer(serializers.ModelSerializer):
    """ Not existing scrape result serializer """
    class Meta:
        """ Meta """
        model = ScrapeResult
        fields = '__all__'
        read_only_fields = ('user',)


class ExistingScrapeResultSerializer(serializers.ModelSerializer):
    """ Existing scrape result serializer """
    class Meta:
        """ Meta """
        model = ScrapeResult
        fields = '__all__'
        read_only_fields = ('keywords_file', 'user',)


class ScrapeResultPageSerializer(serializers.ModelSerializer):
    """ Scrape result page serializer """
    class Meta:
        """ Meta """
        model = ScrapeResultPage
        fields = '__all__'
        read_only_fields = ('keyword', 'source_code', 'result_amount', 'time_taken', 'scrape_result')


class ScrapeResultItemSerializer(serializers.ModelSerializer):
    """ Scrape result item serializer """
    class Meta:
        """ Meta """
        model = ScrapeResultItem
        fields = '__all__'
        read_only_fields = ('title', 'url', 'text', 'is_adwords', 'scrape_result_page')
