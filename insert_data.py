from scrap_package_page import scrap_side_bars
from scrap_package_snippet import get_soup, get_package_details_url,\
    get_packages_snippets_from_page, get_next_page
from create_db import Package, Maintainer, ProgrammingLanguage, NaturalLanguage, OperatingSystem,\
    IntendedAudience, Framework, Environment, Topic
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import SNIPPET_PAGES, DB, START_PAGE, HOME_PAGE

engine = create_engine(DB, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def get_data_dict(n_pages: int = SNIPPET_PAGES, start_page=START_PAGE):
    """ Yields the scraped data as a dict, one by one.

    :param start_page: The page to start scraping from.
    :param n_pages: int, number of pages (each page has 20 packages).
    """
    page_url = start_page
    page = get_soup(page_url)
    for _ in range(n_pages):
        packages_snippets = get_packages_snippets_from_page(page)
        page_url = HOME_PAGE + get_next_page(page)
        page = get_soup(page_url)  # update to the next page
        for packages_snippet in packages_snippets:

            pack_soup = get_soup(get_package_details_url(packages_snippet))
            data = scrap_side_bars(pack_soup, packages_snippet)
            yield data


def name_is_already_in_list(name: str, list_of_dicts: list) -> bool:
    """Given a list of dicts, return true if 'name' is a key of one of the dicts in the list.

    :param name: string - to check if is a key in a dict.
    :param list_of_dicts: A list of dicts.
    :return: True is the 'name' is a key in at least one of the dicts in the list or False otherwise.
    """
    for dict_keys in (d.keys() for d in list_of_dicts):
        if name in dict_keys:
            return True
    return False


def is_email(string):
    """Given a string of info that could be an internal pypi page or an email.
    return True if the string is an email.
    :param string:
    :return:
    """
    return '@' in string


def get_package_data(data_dict: dict) -> dict:
    """Given a dict of the package returns the relevant fields of the package table.

    :param data_dict: dict with package info (that is returned from the scraper).
    :return: a dict with only the relevant fields of the package table.
    """
    start_dict = {'name': None,
                  'version': None,
                  'author': None,
                  'author_info': None,
                  'description': None,
                  'package_license': None,
                  'release_date': None,
                  'github_stars': None,
                  'github_forks': None,
                  'github_open_issues': None}

    package_snippet = next(iter(data_dict.keys()))  # only one

    start_dict['name'] = package_snippet.name
    start_dict['version'] = package_snippet.version
    start_dict['release_date'] = package_snippet.released
    start_dict['description'] = package_snippet.description
    start_dict['description'] = start_dict['description'][:600]
    data = data_dict.values()

    for a_dict in data:
        start_dict['package_license'] = a_dict.get('license')
        if start_dict['package_license'] is not None:
            start_dict['package_license'] = start_dict['package_license'][0]  # the first and only in the list.
        start_dict['github_stars'] = a_dict.get('stars')
        start_dict['github_forks'] = a_dict.get('forks')
        start_dict['github_open_issues'] = a_dict.get('open_issues')
        author = a_dict.get('author')
        if author is not None:
            author = a_dict.get('author')[0]  # list of 1 tuple
            start_dict['author'] = author[0]  # name
            start_dict['author_info'] = author[1]  # info

    return start_dict


def get_maintainers(data_dict: dict) -> list:
    """Given a dict of the package, returns a list of maintainer dicts.

    :param data_dict: dict with package info (that is returned from the scraper).
    :return: A list of maintainer dicts (with keys of:'name', 'email', 'pypi_page').
    """

    maintainer_list = []
    data = data_dict.values()
    for a_dict in data:
        maintainers = a_dict.get('maintainers')  # list zero to many tuples
        if maintainers:
            for maintainer in maintainers:

                man_name = maintainer[0]
                if name_is_already_in_list(man_name, maintainer_list):
                    continue
                man_info = maintainer[1]
                if is_email(man_info):
                    man_mail = man_info
                    man_page = None
                else:
                    man_mail = None
                    man_page = man_info
                maintainer_list.append({'name': man_name, 'email': man_mail, 'pypi_page': man_page})

    return maintainer_list


def create_new_maintainer(maintainer_dict: dict, session_: Session, package) -> None:
    """Adds maintainers to the package package_maintainer. if the maintainer is not
    already in the database in the maintainer table then the code adds the maintainer to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param maintainer_dict: A dict of the maintainer data.
    :param session_: sqlalchemy.orm.session.Session.
    :param package:
    """

    name = maintainer_dict.get('name')
    if name is None:
        name = 'None'
    person_in_db = session_.query(Maintainer).filter(Maintainer.name == name).first()
    if person_in_db:
        package.package_maintainer.append(person_in_db)
    else:
        maintainer = Maintainer(
            name=name, email=maintainer_dict.get('email'), pypi_page=maintainer_dict.get('pypi_page'))
        package.package_maintainer.append(maintainer)


def create_new_environments(data_dict: dict, package, session_: Session = session) -> None:
    """
    Dose NOT COMMIT to the database but only adds to the session.
    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package:
    :param session_: sqlalchemy.orm.session.Session.
    """
    data = data_dict.values()
    for a_dict in data:
        environments = a_dict.get('environment')
        if environments:
            for environment in environments:
                environment_in_db = session_.query(Environment).filter(Environment.environment == environment).first()
                if environment_in_db:
                    package.package_environment.append(environment_in_db)
                else:
                    package.package_environment.append(Environment(environment=environment))


def create_new_programming_languages(data_dict: dict, package, session_: Session = session) -> None:
    """

    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package:
    :param session_: sqlalchemy.orm.session.Session.
    """
    data = data_dict.values()
    for a_dict in data:
        programming_languages = a_dict.get('programming_language')
        if programming_languages:
            for programming_language in programming_languages:
                programming_languages_in_db = session_.query(ProgrammingLanguage).filter(
                    ProgrammingLanguage.programming_language == programming_language).first()
                if programming_languages_in_db:
                    package.package_programming_language.append(programming_languages_in_db)
                else:
                    package.package_programming_language.append(
                        ProgrammingLanguage(programming_language=programming_language))


def create_new_operating_systems(data_dict: dict, package, session_: Session = session) -> None:
    """

    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package:
    :param session_: sqlalchemy.orm.session.Session.
    """
    data = data_dict.values()
    for a_dict in data:
        operating_systems = a_dict.get('operating_system')
        if operating_systems:
            for operating_system in operating_systems:
                operating_systems_in_db = session_.query(OperatingSystem).filter(
                    OperatingSystem.operating_system == operating_system).first()
                if operating_systems_in_db:
                    package.package_operating_system.append(operating_systems_in_db)
                else:
                    package.package_operating_system.append(OperatingSystem(operating_system=operating_system))


def create_new_intended_audiences(data_dict: dict, package, session_: Session = session) -> None:
    """

    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package:
    :param session_: sqlalchemy.orm.session.Session.
    """
    data = data_dict.values()
    for a_dict in data:
        intended_audiences = a_dict.get('intended_audience')
        if intended_audiences:
            for intended_audience in intended_audiences:
                intended_audiences_in_db = session_.query(IntendedAudience).filter(
                    IntendedAudience.intended_audience == intended_audience).first()
                if intended_audiences_in_db:
                    package.package_intended_audience.append(intended_audiences_in_db)
                else:
                    package.package_intended_audience.append(IntendedAudience(intended_audience=intended_audience))


def create_new_frameworks(data_dict: dict, package, session_: Session = session) -> None:
    """

    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package:
    :param session_: sqlalchemy.orm.session.Session.
    """
    data = data_dict.values()
    for a_dict in data:
        frameworks = a_dict.get('framework')
        if frameworks:
            for framework in frameworks:
                framework_in_db = session_.query(Framework).filter(Framework.framework == framework).first()
                if framework_in_db:
                    package.package_framework.append(framework_in_db)
                else:
                    package.package_framework.append(Framework(framework=framework))


def create_new_topics(data_dict: dict, package, session_: Session = session) -> None:
    """

    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package:
    :param session_: sqlalchemy.orm.session.Session.
    :return:
    """

    data = data_dict.values()
    for a_dict in data:
        topics = a_dict.get('topic')
        if topics:
            for topic in topics:
                topic_in_db = session_.query(Topic).filter(Topic.topic == topic).first()
                if topic_in_db:
                    package.package_topic.append(topic_in_db)
                else:
                    package.package_topic.append(Topic(topic=topic))


def create_new_natural_languages(data_dict: dict, package, session_: Session = session) -> None:

    data = data_dict.values()
    for a_dict in data:
        natural_languages = a_dict.get('natural_language')
        if natural_languages:
            for natural_language in natural_languages:
                natural_language_in_db = session_.query(NaturalLanguage).filter(
                    NaturalLanguage.natural_language == natural_language).first()
                if natural_language_in_db:
                    package.package_natural_language.append(natural_language_in_db)
                else:
                    package.package_natural_language.append(NaturalLanguage(natural_language=natural_language))


def insert_or_update_date(n_pages: int = SNIPPET_PAGES, start_page: str = START_PAGE) -> None:
    """Given a number of pages to scrap and a starting page.
    inserts or updates the data to the database.

    :param start_page: The page to start scraping from.
    :param n_pages: int, number of pages (each page has 20 packages).
    """
    for data_dict in get_data_dict(n_pages=n_pages, start_page=start_page):

        package_data = get_package_data(data_dict)
        if not package_data:
            continue
        package_name = package_data.get('name')
        package_in_db = session.query(Package).filter(Package.name == package_name).first()
        if package_in_db:
            if package_data.get('version') == package_in_db.version:
                continue
            else:
                package = session.merge(package_in_db)
                package.version = package_data.get('version')
                package.author = package_data.get('author')
                package.author_info = package_data.get('author_info')
                package.description = package_data.get('description')
                package.package_license = package_data.get('package_license')
                package.release_date = package_data.get('release_date')
                package.github_stars = package_data.get('github_stars')
                package.github_forks = package_data.get('github_forks')
                package.author = package_data.get('github_open_issues')

        else:
            package = Package(**package_data)  # parent table

        # add maintainers
        maintainers_list = get_maintainers(data_dict)
        for maintainer_dict in maintainers_list:
            if maintainer_dict:
                create_new_maintainer(maintainer_dict, session, package)
        # add classifiers
        create_new_programming_languages(data_dict, package)
        create_new_natural_languages(data_dict, package)
        create_new_operating_systems(data_dict, package)
        create_new_intended_audiences(data_dict, package)
        create_new_frameworks(data_dict, package)
        create_new_environments(data_dict, package)
        create_new_topics(data_dict, package)
        session.add(package)  # add parent table to session
        session.commit()  # commit record.


if __name__ == '__main__':
    insert_or_update_date()
