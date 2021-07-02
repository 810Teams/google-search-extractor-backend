"""
    Extractor Application Extraction Script
    extractor/extract.py

    Source
    https://practicaldatascience.co.uk/data-science/how-to-scrape-google-search-results-using-python
"""

import threading
import requests
import urllib
import pandas
from requests_html import HTML, HTMLSession


GOOGLE_DOMAINS = (
    'https://www.google.',
    'https://google.',
    'https://webcache.googleusercontent.',
    'http://webcache.googleusercontent.',
    'https://policies.google.',
    'https://support.google.',
    'https://maps.google.'
)


def get_source(url):
    """ Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)

        return response
    except requests.exceptions.RequestException as e:
        print(e)


def get_response(query, page=None):
    """ Get Google search response """
    if isinstance(page, int):
        return get_source('https://www.google.com/search?q={}&start={}'.format(query, (page - 1) * 10))
    return get_source('https://www.google.com/search?q={}'.format(query))


def scrape_results(query, page=None):
    """ Scrape Google search result page """
    response = get_response(query, page=page)

    # Response Code Error
    if response.status_code != 200:
        print('Error [{}]'.format(response.status_code))
        return None

    # Page data structure
    result_page = {
        'response': response,
        'result_amount': None,
        'time_taken': None,
        'ad_list': list(),
        'result_list': list()
    }
    if isinstance(page, int):
        result_page['page'] = page

    # Result statistics
    stats = response.html.find('#result-stats', first=True).text

    result_page['result_amount'] = int(str().join([i for i in stats.split('\n')[0] if i in '0123456789']))
    result_page['time_taken'] = float(str().join([i for i in stats.split('\n')[1] if i in '0123456789.']))

    # Ads
    ads_list = response.html.find('.cUezCb.luh4tb.O9g5cc.uUPGi')

    for ads in ads_list:
        try:
            result_page['ad_list'].append({
                'title': ads.find('.cfxYMc.JfZTW.c4Djg.MUxGbd.v0nnCb', first=True).text,
                'url': ads.find('.Krnil', first=True).attrs['href'],
                'text': ads.find('.MUxGbd.yDYNvb.lyLwlc', first=True).text
            })
        except AttributeError:
            pass

    # Result Items
    result_list = response.html.find('.tF2Cxc')

    for result in result_list:
        result_page['result_list'].append({
            'title': result.find('h3', first=True).text,
            'url': result.find('.yuRUbf a', first=True).attrs['href'],
            'text': result.find('.IsZvec', first=True).text,
        })

    # Returning
    return result_page
