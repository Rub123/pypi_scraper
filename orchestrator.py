from db.db_functions import *
from scraper.github_api import parse_github_url, get_contributors_number

# session = create_db_session()


def create_a_package_temp_dict():
    """
    The function creates an empty dict with all mandatory keys
    :return: dictionary
    """
    return {'name': None,
            'version': None,
            'author': None,
            'author_info': None,
            'description': None,
            'package_license': None,
            'release_date': None}


def get_github_info(data_dict: dict) -> dict:
    """
    the function receives the dictionary of package information and returns it enriched
    with github information
    :param data_dict: dict with package info (that is returned from the scraper).
    :return: data_dict
    """
    snippet_key = next(iter(data_dict.keys()))
    dict_value = next(iter(data_dict.values()))
    github_url = dict_value.get('github_url')
    if github_url:
        owner, repo = parse_github_url(github_url)
        dict_value['github_contributors'] = get_contributors_number(owner, repo)
    return {snippet_key: dict_value}


def get_package_data(data_dict: dict) -> dict:
    """Given a dict of the package returns the relevant fields of the package table.

    :param data_dict: dict with package info (that is returned from the scraper).
    :return: a dict with only the relevant fields of the package table.
    """
    temp_dict = create_a_package_temp_dict()
    package_snippet = next(iter(data_dict.keys()))  # only one

    temp_dict['name'] = package_snippet.name
    temp_dict['version'] = package_snippet.version
    temp_dict['release_date'] = package_snippet.released
    temp_dict['description'] = package_snippet.description
    temp_dict['description'] = temp_dict['description'][:600]
    data = data_dict.values()

    for a_dict in data:
        temp_dict['package_license'] = a_dict.get('license')
        if temp_dict['package_license'] is not None:
            temp_dict['package_license'] = temp_dict['package_license'][0]  # the first and only in the list.

        author = a_dict.get('author')
        if author is not None:
            author = a_dict.get('author')[0]  # list of 1 tuple
            temp_dict['author'] = author[0]  # name
            temp_dict['author_info'] = author[1]  # info

    return temp_dict


def update_package(package_record_from_db, package_dict, session_):
    """
    # todo finish
    :param package_record_from_db:
    :param package_dict:
    :param session_:
    :return: package
    """
    package = session_.merge(package_record_from_db)
    package.version = package_dict.get('version')
    package.author = package_dict.get('author')
    package.author_info = package_dict.get('author_info')
    package.description = package_dict.get('description')
    package.package_license = package_dict.get('package_license')
    package.release_date = package_dict.get('release_date')
    return package


def add_classifiers(data_dict, package, session_):
    """
    # todo finish
    :param data_dict: dict with package info (that is returned from the scraper).
    :param package:
    :param session_:
    :return: Nothing
    """
    create_new_programming_languages(data_dict, package, session_)
    create_new_natural_languages(data_dict, package, session_)
    create_new_operating_systems(data_dict, package, session_)
    create_new_intended_audiences(data_dict, package, session_)
    create_new_frameworks(data_dict, package, session_)
    create_new_environments(data_dict, package, session_)
    create_new_topics(data_dict, package, session_)
    create_new_github_info(data_dict, package, session_)


def insert_or_update_date(data_dict, session_=None) -> None:
    """Given a number of pages to scrap and a starting page.
    inserts or updates the data to the database.

    :param data_dict: dict with package info (that is returned from the scraper).
    :param session_: Nothing
    """
    session_ = create_db_session() if session_ is None else session_
    package_data = get_package_data(data_dict)
    if not package_data:
        return None
    package_name = package_data.get('name')
    package_in_db = session_.query(Package).filter(Package.name == package_name).first()
    if package_in_db:
        if package_data.get('version') == package_in_db.version:
            return None  # already in updated in the database.
        else:
            package = update_package(package_in_db, package_data, session_)
    else:
        package = Package(**package_data)  # parent table

    # add maintainers
    maintainers_list = get_maintainers(data_dict)
    for maintainer_dict in maintainers_list:
        if maintainer_dict:
            create_new_maintainer(maintainer_dict, session_, package)
    # add classifiers
    add_classifiers(data_dict, package, session_)

    session_.add(package)  # add parent table to session
    session_.commit()  # commit record.
