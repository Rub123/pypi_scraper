from db.db_functions import *

# session = create_db_session()


def create_a_package_temp_dict():
    return {'name': None,
            'version': None,
            'author': None,
            'author_info': None,
            'description': None,
            'package_license': None,
            'release_date': None,
            'github_stars': None,
            'github_forks': None,
            'github_open_issues': None}


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
        temp_dict['github_stars'] = a_dict.get('stars')
        temp_dict['github_forks'] = a_dict.get('forks')
        temp_dict['github_open_issues'] = a_dict.get('open_issues')
        author = a_dict.get('author')
        if author is not None:
            author = a_dict.get('author')[0]  # list of 1 tuple
            temp_dict['author'] = author[0]  # name
            temp_dict['author_info'] = author[1]  # info

    return temp_dict


def update_package(package_record_from_db, package_dict, session_):
    package = session_.merge(package_record_from_db)
    package.version = package_dict.get('version')
    package.author = package_dict.get('author')
    package.author_info = package_dict.get('author_info')
    package.description = package_dict.get('description')
    package.package_license = package_dict.get('package_license')
    package.release_date = package_dict.get('release_date')
    package.github_stars = package_dict.get('github_stars')
    package.github_forks = package_dict.get('github_forks')
    package.author = package_dict.get('github_open_issues')
    return package


def add_classifiers(data_dict, package, session_):
    create_new_programming_languages(data_dict, package, session_)
    create_new_natural_languages(data_dict, package, session_)
    create_new_operating_systems(data_dict, package, session_)
    create_new_intended_audiences(data_dict, package, session_)
    create_new_frameworks(data_dict, package, session_)
    create_new_environments(data_dict, package, session_)
    create_new_topics(data_dict, package, session_)


def insert_or_update_date(data_dict, session_=None) -> None:
    """Given a number of pages to scrap and a starting page.
    inserts or updates the data to the database.

    :param data_dict:
    :param session_:
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
