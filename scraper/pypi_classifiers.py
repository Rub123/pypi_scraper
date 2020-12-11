import configparser
import requests
from collections import defaultdict
from bs4 import BeautifulSoup

config1 = configparser.ConfigParser()
config1.read('config.ini')
keys = config1.keys()
print('==>', config1.sections())


def get_classifier_info():
    config = configparser.ConfigParser()
    config.read('config.ini')
    p_page = config['classifiers']['PAGE']
    p_headers = config['requests']['headers']
    p_timeout = config['requests']['timeout']
    p_classifier_index = config['classifiers']['CLASSIFIER_INDEX']
    return p_page, p_headers, p_timeout, p_classifier_index


def get_soup(url: str) -> BeautifulSoup:
    """
    Get a BeautifulSoup object from a given url.
    :param url: url as string to get in BeautifulSoup from
    :return: BeautifulSoup object
    """
    _, headers, timeout, _ = get_classifier_info()
    print(url)
    response: requests.Response = requests.get(url, headers=headers,  timeout=timeout)
    return BeautifulSoup(response.content, 'html.parser')


def get_all_classifiers(url) -> dict:
    """
    Create a dictionary with all optional classifiers that are available in pypi as defined in the classifiers PAGE
    :param url: Link to the classifier page of pypi, defaults to PAGE.
    :return: a dictionary of all available classifiers
    """
    _, classifier_index, _, _ = get_classifier_info()
    soup = get_soup(url)
    div = soup.find('div', class_='narrow-container')
    ul = div.find('ul')

    classifiers_dict = defaultdict(set)

    for li in ul.find_all('li'):
        classifier_type,  *classifier_type_values = li.text.split('\n')[classifier_index].split(' :: ', 1)
        classifiers_dict[classifier_type].add(''.join(classifier_type_values))

    return classifiers_dict


if __name__ == '__main__':
    url_class, _, _, _ = get_classifier_info()
    classifiers = get_all_classifiers(url_class)
    for key, value in classifiers.items():
        print(key, value)
