import requests
from datetime import datetime
from collections import namedtuple, defaultdict
from bs4 import BeautifulSoup
import bs4
from pprint import pprint
from typing import List
from pypi_classifiers import PAGE as CLASSIFIERS_PAGE
from pypi_classifiers import get_all_classifiers
import pickle

HOME_PAGE = "https://pypi.org"
START_PAGE = pypi_url = "https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3"

PackageSnippet = namedtuple('PackageSnippet',
                            'name version link released description')


PackageSnippetList = List[PackageSnippet]


def get_soup(url: str) -> BeautifulSoup:
    response: requests.Response = requests.get(url)
    # TODO add response error handling
    return BeautifulSoup(response.content, 'html.parser')


def parse_released(tag_: bs4.element.Tag) -> datetime.date:
    # the datetime data from pypi is not consistent in its format.
    # instead of leaving it as strings, this code will parse a date object (discarded the time info.)
    released = tag_.contents[0].get('datetime')[:10]
    return datetime.strptime(released, '%Y-%m-%d').date()


def get_next_page(page: BeautifulSoup) -> str:
    button_group = page.find_all('a', class_='button button-group__button')
    for button in reversed(button_group):
        if button.text == 'Next':
            return button.get('href')


def get_packages_snippets_from_page(page: BeautifulSoup) -> PackageSnippetList:
    packages = page.find_all('a', class_='package-snippet')
    packages_links = [PackageSnippet(
                       package.find('span', class_='package-snippet__name').text,
                       package.find('span', class_='package-snippet__version').text,
                       package.get('href'),
                       parse_released(package.find('span', class_='package-snippet__released')),
                       package.find('p', class_='package-snippet__description').text)

                      for package in packages]
    return packages_links


def get_n_pages_of_packages_snippets(n_pages: int, start_page: BeautifulSoup) -> PackageSnippetList:
    packages_snippets = []
    page = start_page
    for _ in range(n_pages):
        packages_snippets.extend(get_packages_snippets_from_page(page))
        page_url = HOME_PAGE + get_next_page(page)
        page = get_soup(page_url)

    return packages_snippets


def get_package_details_url(package_snippet: PackageSnippet) -> str:
    return HOME_PAGE + package_snippet.link


if __name__ == '__main__':
    start_soup = get_soup(START_PAGE)
    while True:
        try:
            pages = int(input('How many pages to scrape? '))
            break
        except ValueError:
            print('Try again!')
    pages = pages if pages else 1
    packs_snips = get_n_pages_of_packages_snippets(pages, start_soup)
    packs_urls = (get_package_details_url(pack) for pack in packs_snips)
    # packs_soups = (get_soup(get_package_details_url(pack)) for pack in packs_snips)
    for pack_snip, pack_url in zip(packs_snips, packs_urls):
        print(pack_snip)
        print(pack_url)
        print('-' * 100)
