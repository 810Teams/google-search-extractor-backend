"""
    Extractor Application Models
    extractor/models.py
"""

import threading
import time

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models

from core.util.objects import save_user_attributes
from core.util.misc import get_file_extension, get_simpler_datetime
from extractor.extract import scrape_results
from google_search_extractor_backend.settings import STORAGE_BASE_DIR, DELAY_BETWEEN_PAGES


class ScrapeResult(models.Model):
    """ Scrape result """
    def get_keywords_file_path(self, file_name):
        """ Get uploaded keywords file path """
        return '{}/scrape_result/{}/keywords.{}'.format(STORAGE_BASE_DIR, self.id, get_file_extension(file_name))

    def get_report_path(self, _):
        """ Get uploaded keywords file path """
        return '{}/scrape_result/{}/report.xml'.format(STORAGE_BASE_DIR, self.id)

    # Files
    keywords_file = models.FileField(upload_to=get_keywords_file_path, null=False, blank=False)
    keyword_amount = models.IntegerField(null=False, blank=True)
    report = models.FileField(upload_to=get_report_path, null=True, blank=True)

    # Stamps
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ String representation """
        return 'ScrapeResult object ({}) ({}, {})'.format(
            self.id, self.user.__str__(), get_simpler_datetime(str(self.created_at))
        )

    def save(self, *args, **kwargs):
        """ Save instance """
        save_user_attributes(self, created_by_field_name='user', updated_by_field_name=None)

        # Scrape result page generation
        keywords = [[j.strip() for j in i.decode('utf-8').split(',')] for i in self.keywords_file]
        flatten = lambda t: [item for sublist in t for item in sublist]
        keywords = flatten(keywords)

        if len(ScrapeResultPage.objects.filter(scrape_result_id=self.id)) == 0:
            thread = threading.Thread(target=self.create_scrape_result_pages, args=[keywords])
            thread.start()

        # Keyword Amount Saving
        self.keyword_amount = len(keywords)

        # Save keywords file
        if self.pk is None:
            saved_keywords_file = self.keywords_file
            self.keywords_file = None
            super(ScrapeResult, self).save(*args, **kwargs)
            self.keywords_file = saved_keywords_file

            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(ScrapeResult, self).save(*args, **kwargs)

    def create_scrape_result_pages(self, keywords):
        """ Create scrape result page """
        time_start = time.time()
        report_content = [
            '<?xml version="1.0" encoding="UTF-8" ?>',
            '',
            '<scrape-result>',
            '\t<general-info>',
            '\t\t<id>{}</id>'.format(self.id),
            '\t\t<user-id>{}</user-id>'.format(self.user.id),
            '\t\t<user-username>{}</user-username>'.format(self.user.username),
            '\t\t<created-at>{}</created-at>'.format(get_simpler_datetime(str(self.created_at))),
            '\t\t<time-taken>{}</time-taken>',
            '\t\t<keyword-amount>{}</keyword-amount>'.format(len(keywords)),
            '\t</general-info>',
            '',
            '\t<scrape-result-page-list>',
        ]

        for i in keywords:
            # Scrape result
            result_page = scrape_results(i)
            if result_page is None:
                break

            # Create scrape result page object
            scrape_result_page = ScrapeResultPage.objects.create(
                keyword=i,
                source_code=ContentFile(result_page['response'].content, name='source_code.html'),
                result_amount=result_page['result_amount'],
                time_taken=result_page['time_taken'],
                scrape_result_id=self.id
            )

            # Report - Part 1
            report_content += [
                '\t\t<scrape-result-page>',
                '\t\t\t<keyword>{}</keyword>'.format(i),
                '\t\t\t<adwords-result-amount>{}</adwords-result-amount>',
                '\t\t\t<non-adwords-result-amount>{}</non-adwords-result-amount>',
                '\t\t\t<scrape-result-item-list>'
            ]

            # Create scrape result item object (AdWords)
            for j in result_page['ad_list']:
                scrape_result_item = ScrapeResultItem.objects.create(
                    title=j['title'], url=j['url'], text=j['text'], is_adwords=True,
                    scrape_result_page_id=scrape_result_page.id
                )
                # Report - Part 2.1
                report_content += [
                    '\t\t\t\t<scrape-result-item>',
                    '\t\t\t\t\t<title>![CDATA[{}]]</title>'.format(scrape_result_item.title),
                    '\t\t\t\t\t<url>![CDATA[{}]]</url>'.format(scrape_result_item.url),
                    '\t\t\t\t\t<text>![CDATA[{}]]</text>'.format(scrape_result_item.text),
                    '\t\t\t\t\t<is-adwords>1</is-adwords>',
                    '\t\t\t\t</scrape-result-item>'
                ]

            # Create scrape result item object (Non-AdWords)
            for j in result_page['result_list']:
                scrape_result_item = ScrapeResultItem.objects.create(
                    title=j['title'], url=j['url'], text=j['text'], is_adwords=False,
                    scrape_result_page_id=scrape_result_page.id
                )
                # Report - Part 2.2
                report_content += [
                    '\t\t\t\t<scrape-result-item>',
                    '\t\t\t\t\t<title><![CDATA[{}]]></title>'.format(scrape_result_item.title.replace('\n', str())),
                    '\t\t\t\t\t<url><![CDATA[{}]]></url>'.format(scrape_result_item.url.replace('\n', str())),
                    '\t\t\t\t\t<text><![CDATA[{}]]></text>'.format(scrape_result_item.text.replace('\n', str())),
                    '\t\t\t\t\t<is-adwords>0</is-adwords>',
                    '\t\t\t\t</scrape-result-item>'
                ]

            # Report - Part 3
            report_content += [
                '\t\t\t</scrape-result-item-list>',
                '\t\t</scrape-result-page>'
            ]

            # Report - Part 4
            _ = report_content.index('\t\t\t<adwords-result-amount>{}</adwords-result-amount>')
            report_content[_] = report_content[_].format(
                len(ScrapeResultItem.objects.filter(scrape_result_page_id=scrape_result_page.id, is_adwords=True))
            )
            _ = report_content.index('\t\t\t<non-adwords-result-amount>{}</non-adwords-result-amount>')
            report_content[_] = report_content[_].format(
                len(ScrapeResultItem.objects.filter(scrape_result_page_id=scrape_result_page.id, is_adwords=False))
            )

            # Delay (seconds)
            time.sleep(DELAY_BETWEEN_PAGES)

        # Report - Ending
        report_content += [
            '\t</scrape-result-page-list>',
            '</scrape-result>',
            ''
        ]
        _ = report_content.index('\t\t<time-taken>{}</time-taken>')
        report_content[_] = report_content[_].format(time.time() - time_start)

        # Save Report
        self.report = ContentFile(('\n\r'.join(report_content)).encode('utf-8'), name='report.xml')
        self.save()


class ScrapeResultPage(models.Model):
    """ Scrape result page model """
    def get_source_code_path(self, _):
        """ Get source code path """
        return '{}/scrape_result/{}/{}/source_code.html'.format(STORAGE_BASE_DIR, self.scrape_result.id, self.keyword)

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
