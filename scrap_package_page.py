import requests
from collections import defaultdict
from bs4 import BeautifulSoup, element

from scrap_package_snippet import PackageSnippet
from pypi_classifiers import PAGE as CLASSIFIERS_PAGE
from pypi_classifiers import get_all_classifiers


# titles of information available in sidebar sections
# ['Navigation', 'Project links', 'Statistics', 'Meta', 'Maintainers', 'Classifiers']

SKIP_SECTIONS = 'Navigation', 'Project links'  # sections we decided to skip and not scarp information


def get_meta(sidebar_section_div: element.Tag) -> dict:
    """Getting Author info from the meta sidebar section (if available).

    :param sidebar_section_div: div bs4.element.Tag with the relevant meta data.
    :return: A dict with the author tuple of name and info (info could be a link the author
    page in pypi or an email. if not available will return a dict with None values.
    """
    result_dict = {'author': None}
    for p_tag in sidebar_section_div.find_all('p'):
        p_tag: element.Tag
        for strong_tag in p_tag.find_all('strong'):
            meta_section = strong_tag.text.rstrip(':')
            if meta_section == 'License':
                continue  # The license is scraped from the classifiers section.
            elif meta_section == 'Author':
                author = p_tag.find('a')
                if author:
                    author_mail = author.get('href')
                    author_name = author.text
                    result_dict['author'] = [(author_name, author_mail)]
    return result_dict


def get_maintainers(sidebar_section_div: element.Tag) -> dict:
    """Getting maintainers list from maintainers sidebar section (if available).

    :param sidebar_section_div: div bs4.element.Tag with the relevant maintainers data.
    :return: A dict with key 'maintainers', and the value is a list of tuples of maintainer_name,
     maintainer_info where the info could be an email or an internal link to the maintainer page in pypi.
    """
    maintainers = defaultdict(list)
    for maintainer_section in sidebar_section_div.find_all('span', class_='sidebar-section__maintainer'):
        maintainer_name = maintainer_section.text.strip()
        maintainer_name_link = maintainer_section.find('a')
        maintainer_info = None if not maintainer_name_link else maintainer_name_link.get('href')
        maintainers['maintainers'].append((maintainer_name, maintainer_info))
    return dict(maintainers)


def get_statistics(sidebar_section_div: element.Tag) -> dict:
    """Getting statistics (stars, forks, open_issues)  from github (if available).

    :param sidebar_section_div: div bs4.element.Tag with the relevant statistics data.
    :return: A dict with github statistics metrics (stars, forks, open issues).
    """
    statistics = {'stars': None, 'forks': None, 'open_issues': None}
    for github_div in sidebar_section_div.find_all('div', class_='github-repo-info'):
        if github_div:
            data_url = github_div.get('data-url')
            json_data = requests.get(data_url).json()
            if 'message' in json_data.keys() and len(json_data.keys()) == 2:
                # no data
                continue
            else:
                statistics['stars'] = json_data.get('stargazers_count')
                statistics['forks'] = json_data.get('forks')
                statistics['open_issues'] = json_data.get('open_issues_count')
                break
    return statistics


# helper functions for getting the classifiers from the package page.
def get_classifiers_set() -> set:
    """Returns a set of all available classifiers from the CLASSIFIERS_PAGE of pypi in pep8 format"""
    classifiers_dict = get_all_classifiers(CLASSIFIERS_PAGE)
    return {classifier.strip().lower().replace(' ', '_') for classifier in classifiers_dict.keys()}


def make_classifier_key(key: str) -> str:
    """Converts the classifier keys in a specific page to a proper pep8 string keys"""
    return key.strip().lower().replace(' ', '_')


def get_classifiers(sidebar_section_div: element.Tag) -> dict:
    """
    Get classifiers that are mentioned in a page
    and return dictionary with the relevant available information from the page.
    :param sidebar_section_div: gets the div of the sidebar in a current page
    :return: A dict with classifier as key and a list of classifier as value.
    """

    classifiers_set = get_classifiers_set()
    classifiers = defaultdict(list)
    for ul_tag in sidebar_section_div.find_all('ul', class_='sidebar-section__classifiers'):
        for child_tag in ul_tag.children:
            if not isinstance(child_tag, element.Tag):
                continue
            classifier_name = child_tag.find('strong').text.strip()
            classifier_key = make_classifier_key(classifier_name)
            if classifier_key not in classifiers_set:
                continue
            for classifier_value in child_tag.find_all('a'):
                classifiers[classifier_key].append(classifier_value.text.strip())

    return dict(classifiers)


# define a dictionary that holds as key the title of the side bar info, and as value the function you need to scarp it
sidebar_section_getters = {
    # 'Navigation': None,
    # 'Project links': None,
    'Statistics': get_statistics,
    'Meta': get_meta,
    'Maintainers': get_maintainers,
    'Classifiers': get_classifiers

}


def scrap_side_bars(pack_soup: BeautifulSoup, pack_snippet: PackageSnippet):
    """
    Get the actual data from the side bar of the page (ignores Navigation and project links)
    and return a dict with the information that is available for the package given package (not all pages has all
    the optional information)
    the function uses the dict sidebar_section_getters to know which function to call in order to scarp the info
    of that specific section
    :param pack_soup: BeautifulSoup object
    :param pack_snippet: PackageSnippet, information scarped from the snippet element
    :return: dict with the available information for a specific package
    """
    data = {pack_snippet: {}}
    for div in pack_soup.find_all('div', class_='sidebar-section'):
        sidebar_title = div.find('h3', class_='sidebar-section__title').text
        if sidebar_title in SKIP_SECTIONS:
            continue
        data[pack_snippet].update(sidebar_section_getters[sidebar_title](div))
    return data
