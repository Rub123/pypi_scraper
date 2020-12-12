from pathlib import Path
from scraper.scrap_package_snippet import get_packages_snippets_from_page, get_next_page, \
    get_package_details_url
from scraper.scrap_package_page import scrap_side_bars
from scraper.scrape_logger import PYPI_LOGGER
from time import sleep
import requests
from requests.exceptions import Timeout
import sys
import configparser
from bs4 import BeautifulSoup


config = configparser.ConfigParser(interpolation=None)
config.read(Path('config.ini').absolute())

HEADERS = {config['requests']['headers_key']: config['requests']['headers_val']}
TIMEOUT = int(config['requests']['timeout'])
HOME_PAGE = config['pypi']['HOME_PAGE']
SNIPPET_PAGES = config['scraper']['SNIPPET_PAGES']
START_PAGE = config['pypi']['START_PAGE']
N_TRIES = int(config['timeout']['n_tries'])
SLEEP = int(config['timeout']['sleep'])


def timeout_handler(page_url: str, n_tries: int = N_TRIES, sleep_: int = SLEEP) -> BeautifulSoup:
    """In case of a timeout error when requesting a url, will try n_tries times.
    After each time will wait sleep_ seconds before trying again.

    :param page_url: A url string to request.
    :param n_tries: Number of times (int) to try before quiting.
    :param sleep_: Number of seconds to wait before trying again.
    :return:
    """
    tries = 0
    while tries < n_tries:
        try:
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, 'html.parser')
        except Timeout as ex:
            PYPI_LOGGER.error(ex)
            sleep(sleep_)
            tries += 1
            continue

        else:
            PYPI_LOGGER.info(f'successfully requested and souped {page_url}')
            return soup
    print(f'Time out Error have occurred for a few times when trying to request {page_url}.')
    print(f'Please try again in another time.')
    sys.exit(-1)


def get_data_dict(n_pages: int = SNIPPET_PAGES, start_page: str = START_PAGE):
    """ Yields the scraped data as a dict, one by one.

    :param start_page: The page to start scraping from.
    :param n_pages: int, number of pages (each page has 20 packages).
    """
    page_url = start_page
    try:
        page = timeout_handler(page_url)
    except requests.exceptions.RequestException as ex:
        PYPI_LOGGER.critical(f'start_page: {start_page} request err: {ex}')
        print(f'Error requesting {start_page}')
        print('Sorry, Bye.')
        sys.exit(-1)
    for _ in range(n_pages):
        packages_snippets = get_packages_snippets_from_page(page)
        page_url = HOME_PAGE + get_next_page(page)
        try:
            page = timeout_handler(page_url)  # update to the next page
        except requests.exceptions.RequestException as ex:
            PYPI_LOGGER.error(ex)
            continue
        for packages_snippet in packages_snippets:
            try:
                pack_soup = timeout_handler(get_package_details_url(packages_snippet))
            except requests.exceptions.RequestException as ex:
                PYPI_LOGGER.error(ex)
                continue
            data = scrap_side_bars(pack_soup, packages_snippet)
            yield data
