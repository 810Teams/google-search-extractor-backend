"""
    Extractor Application Models
    extractor/models.py
"""

from django.contrib.auth import get_user_model
from django.db import models

from core.util.objects import get_file_extension, save_user_attributes
from google_search_extractor_backend.settings import STORAGE_BASE_DIR


class ScrapeResult(models.Model):
    """ Scrape result """
    def get_keywords_file_path(self, file_name):
        """ Get uploaded keywords file path """
        return '{}/scrape_result/{}/keywords.{}'.format(STORAGE_BASE_DIR, self.pk, get_file_extension(file_name))

    def get_report_path(self, _):
        """ Get uploaded keywords file path """
        return '{}/scrape_result/{}/report.txt'.format(STORAGE_BASE_DIR, self.pk)

    # Files
    keywords_file = models.FileField(upload_to=get_keywords_file_path, null=True, blank=False)

    # Stamps
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Save instance """
        save_user_attributes(self, created_by_field_name='user', updated_by_field_name=None)

        if self.pk is None:
            saved_keywords_file = self.keywords_file
            self.keywords_file = None
            super(ScrapeResult, self).save(*args, **kwargs)
            self.keywords_file = saved_keywords_file

            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        # TODO: Add generate report

        super(ScrapeResult, self).save(*args, **kwargs)


class ScrapeResultPage(models.Model):
    """ Scrape result page model """
    def get_source_code_path(self, _):
        """ Get source code path """
        return '{}/scrape_result/{}/source_code.html'.format(STORAGE_BASE_DIR, self.pk)

    keyword = models.CharField(max_length=64)
    source_code = models.FileField(upload_to=get_source_code_path, null=False, blank=True)
    result_amount = models.IntegerField()
    time_taken = models.FloatField()
    scrape_result = models.ForeignKey(ScrapeResult, on_delete=models.CASCADE)


class ScrapeResultItem(models.Model):
    """ Scrape result item model """
    title = models.CharField(max_length=255)
    url = models.URLField()
    text = models.TextField(max_length=1024)
    is_adwords = models.BooleanField(default=False)
    scrape_result_page = models.ForeignKey(ScrapeResultPage, on_delete=models.CASCADE)
