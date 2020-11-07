import requests
from collections import defaultdict
from bs4 import BeautifulSoup

PAGE = 'https://pypi.org/classifiers/'
CLASSIFIER_INDEX = 1


def get_soup(url: str) -> BeautifulSoup:
    # todo add docstrings
    response: requests.Response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


def get_all_classifiers(url=PAGE) -> dict:
    # todo add docstrings
    soup = get_soup(url)
    div = soup.find('div', class_='narrow-container')
    ul = div.find('ul')

    classifiers_dict = defaultdict(set)

    for li in ul.find_all('li'):
        classifier_type,  *classifier_type_values = li.text.split('\n')[CLASSIFIER_INDEX].split(' :: ')
        classifiers_dict[classifier_type].add(''.join(classifier_type_values))

    return classifiers_dict


if __name__ == '__main__':
    classifiers = get_all_classifiers()
    for key, value in classifiers.items():
        print(key, value)
