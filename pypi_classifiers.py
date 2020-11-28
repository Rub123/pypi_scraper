import requests
from collections import defaultdict
from bs4 import BeautifulSoup

from config import PAGE, CLASSIFIER_INDEX


def get_soup(url: str) -> BeautifulSoup:
    """
    Get a BeautifulSoup object from a given url.
    :param url: url as string to get in BeautifulSoup from
    :return: BeautifulSoup object
    """
    response: requests.Response = requests.get(url)
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


if __name__ == '__main__':
    classifiers = get_all_classifiers()
    for key, value in classifiers.items():
        print(key, value)
