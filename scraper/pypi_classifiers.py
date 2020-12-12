import configparser
from pathlib import Path
import requests
from collections import defaultdict
from bs4 import BeautifulSoup


config = configparser.ConfigParser()
config.read(Path('config.ini'))
PAGE = config['classifiers']['PAGE']
HEADERS = {config['requests']['headers_key']: config['requests']['headers_val']}
TIMEOUT = int(config['requests']['timeout'])
CLASSIFIER_INDEX = int(config['classifiers']['CLASSIFIER_INDEX'])


def get_soup(url: str) -> BeautifulSoup:
    """
    Get a BeautifulSoup object from a given url.
    :param url: url as string to get in BeautifulSoup from
    :return: BeautifulSoup object
    """
    response: requests.Response = requests.get(url, headers=HEADERS,  timeout=TIMEOUT)
    return BeautifulSoup(response.content, 'html.parser')


def get_all_classifiers(url=PAGE) -> dict:
    """
    Create a dictionary with all optional classifiers that are available in pypi as defined in the classifiers PAGE
    :param url: Link to the classifier page of pypi, defaults to PAGE.
    :return: a dictionary of all available classifiers
    """
    soup = get_soup(url)
    div = soup.find('div', class_='narrow-container')
    ul = div.find('ul')

    classifiers_dict = defaultdict(set)

    for li in ul.find_all('li'):
        classifier_type,  *classifier_type_values = li.text.split('\n')[CLASSIFIER_INDEX].split(' :: ', 1)
        classifiers_dict[classifier_type].add(''.join(classifier_type_values))

    return classifiers_dict
