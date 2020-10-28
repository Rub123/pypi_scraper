import requests
from datetime import datetime
from collections import namedtuple
from bs4 import BeautifulSoup
import bs4
from typing import List


HOME_PAGE = "https://pypi.org"


PackageSnippet = namedtuple('PackageSnippet',
                            'name version link released description')


PackageSnippetList = List[PackageSnippet]
# python projects sorted by date last updated
pypi_url = "https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3"


def parse_released(tag_: bs4.element.Tag):
    # todo - add docstring
    # the datetime data from pypi is not consistent in its format.
    # instead of leaving it as strings, this code will parse a date object (discarded the time info.)
    released = tag_.contents[0].get('datetime')[:10]
    return datetime.strptime(released, '%Y-%m-%d').date()


html = requests.get(pypi_url)
soup = BeautifulSoup(html.content, 'html.parser')

# print(soup.prettify())


def get_soup(url: str) -> BeautifulSoup:
    # todo - add docstring
    response: requests.Response = requests.get(url)
    # TODO add response error handling
    return BeautifulSoup(response.content, 'html.parser')


def get_next_page(page: BeautifulSoup):
    # todo - add docstring
    button_group = page.find_all('a', class_='button button-group__button')
    for button in reversed(button_group):
        if button.text == 'Next':
            return button.get('href')


def get_packages_snippets_from_page(page: BeautifulSoup) -> PackageSnippetList:
    # todo - add docstring
    packages = page.find_all('a', class_='package-snippet')
    packages_links = [PackageSnippet(
                       package.find('span', class_='package-snippet__name').text,
                       package.find('span', class_='package-snippet__version').text,
                       package.get('href'),
                       parse_released(package.find('span', class_='package-snippet__released')),
                       package.find('p', class_='package-snippet__description').text)

                      for package in packages]
    return packages_links


def get_n_pages_of_packages_snippets(n_pages: int, start_page: BeautifulSoup = soup) -> PackageSnippetList:
    # todo - add docstring
    packages_snippets = []
    page = start_page
    for _ in range(n_pages):
        packages_snippets.extend(get_packages_snippets_from_page(page))
        page_url = HOME_PAGE + get_next_page(page)
        page = get_soup(page_url)

    return packages_snippets


packs = get_n_pages_of_packages_snippets(3)

for pack in packs:
    print(pack)

print(len(packs))
