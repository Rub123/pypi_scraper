import requests
from datetime import datetime
from collections import namedtuple
from bs4 import BeautifulSoup, element
from typing import List

HOME_PAGE = "https://pypi.org"
START_PAGE = pypi_url = "https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3"
NUMBER_OF_SEP_CHARS = 100  # When printing the info for a package - will use a separator  char between each pack.

# A named tuple class to hold the package snippet info.
PackageSnippet = namedtuple('PackageSnippet',
                            'name version link released description')

# Aliasing type hints for a list of Package snippets.
PackageSnippetList = List[PackageSnippet]


def get_soup(url: str) -> BeautifulSoup:
    """Todo add docstring"""
    response: requests.Response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


def parse_released(tag_: element.Tag) -> datetime.date:
    """Todo add docstring"""
    # the datetime data from pypi is not consistent in its format.
    # instead of leaving it as strings, this code will parse a date object (discarded the time info.)
    released = tag_.contents[0].get('datetime')[:10]
    return datetime.strptime(released, '%Y-%m-%d').date()


def get_next_page(page: BeautifulSoup) -> str:
    """Todo add docstring"""
    button_group = page.find_all('a', class_='button button-group__button')
    for button in reversed(button_group):
        if button.text == 'Next':
            return button.get('href')


def get_packages_snippets_from_page(page: BeautifulSoup) -> PackageSnippetList:
    """Todo add docstring"""
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
    """Todo add docstring"""
    packages_snippets = []
    page = start_page
    for _ in range(n_pages):
        packages_snippets.extend(get_packages_snippets_from_page(page))
        page_url = HOME_PAGE + get_next_page(page)
        page = get_soup(page_url)

    return packages_snippets


def get_package_details_url(package_snippet: PackageSnippet) -> str:
    """Todo add docstring"""
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
    for pack_snip, pack_url in zip(packs_snips, packs_urls):
        print(pack_snip)
        print(pack_url)
        print('-' * NUMBER_OF_SEP_CHARS)
