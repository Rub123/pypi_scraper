import requests
from dataclasses import dataclass
from datetime import datetime

from collections import namedtuple
from bs4 import BeautifulSoup
import bs4
from typing import List, NamedTuple

HOME_PAGE = "https://pypi.org"

# class PackageSnippet:
#     def __init__(self, name, version, link, released, description):
#         self.name = name
#         self.version = version
#         self.link = ''


# def create_package_snippet(name, version, rel_link, released, description):
#     link = HOME_PAGE + rel_link
#     released =
#     package = PackageSnippet(
#
#     )

PackageSnippet = namedtuple('PackageSnippet',
                            'name version link released description')

# python projects sorted by date last updated
pypi_url = "https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3"


# def parse_released(tag_: bs4.element.Tag):
#     released = tag_.contents[0].get('datetime').rstrip('+0000')
#     # one some dates wont parse because the seconds string is one digit (and not 2)
#     released = released + '0' if len(released) == 18 else released
#     return datetime.fromisoformat(released)

def parse_released(tag_: bs4.element.Tag):
    # the datetime data from pypi is not consistent in its format.
    # instead of leaving it as strings, this parse a date object discarded the time info.
    released = tag_.contents[0].get('datetime')[:10]
    return datetime.strptime(released, '%Y-%m-%d').date()


html = requests.get(pypi_url)
soup = BeautifulSoup(html.content, 'html.parser')
packages = soup.find_all('a', class_='package-snippet')
print(packages[0])
packages_links = [PackageSnippet(
                   package.find('span', class_='package-snippet__name').text,
                   package.find('span', class_='package-snippet__version').text,
                   package.get('href'),
                   parse_released(package.find('span', class_='package-snippet__released')),
                   package.find('p', class_='package-snippet__description').text)

                  for package in packages]



test: bs4.element.Tag = soup.find_all('a', class_='package-snippet')[0]
x: bs4.element.Tag = test.find('span', class_='package-snippet__released')
print((x.contents[0].get('datetime')))
print(len(packages_links), packages_links)
