"""
    Extractor Application Django Admin
    extractor/admin.py
"""

from django.contrib import admin

from extractor.models import ScrapeResult, ScrapeResultPage, ScrapeResultItem


class ScrapeResultAdmin(admin.ModelAdmin):
    """ Scrape result admin """
    list_display = ('id', 'keywords_file', 'keyword_amount', 'user', 'created_at')
    list_per_page = 20


class ScrapeResultPageAdmin(admin.ModelAdmin):
    """ Scrape result page admin """
    list_display = ('id', 'scrape_result', 'keyword', 'source_code', 'result_amount', 'time_taken')
    list_per_page = 20


class ScrapeResultItemAdmin(admin.ModelAdmin):
    """ Scrape result item admin """
    list_display = ('id', 'title', 'url', 'is_adwords', 'scrape_result_page')
    list_per_page = 20


admin.site.register(ScrapeResult, ScrapeResultAdmin)
admin.site.register(ScrapeResultPage, ScrapeResultPageAdmin)
admin.site.register(ScrapeResultItem, ScrapeResultItemAdmin)
