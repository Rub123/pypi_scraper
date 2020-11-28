from scrap_package_page import scrap_side_bars
from scrap_package_snippet import PackageSnippet, get_soup, get_n_pages_of_packages_snippets, \
    get_package_details_url, get_packages_snippets_from_page, get_next_page
from scrap_package_snippet import START_PAGE, HOME_PAGE
from create_db2 import Package, Maintainer, ProgrammingLanguage, NaturalLanguage, OperatingSystem,\
    IntendedAudience, Framework, Environment, Topic

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy import create_engine
from config import SNIPPET_PAGES, PACKAGE_SEPARATORS_CHARS, DB
from scrap_package_page import make_classifier_key
from pypi_classifiers import get_all_classifiers

engine = create_engine(DB, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

classifiers = {make_classifier_key(key): value for key, value in get_all_classifiers().items()}
# create a Session


def get_classifier_dict(table_class, classifier: str, session_: Session = session) -> dict:
    """Given a classifier table class, returns a dict with the classifier values as keys and the rows id's as values.

    :param table_class: Classifier table of type 'sqlalchemy.ext.declarative.api.DeclarativeMeta'
    :param classifier: The name of the classifier in the table
    :param session_: sqlalchemy.orm.session.Session.
    :return: A dict with the classifier values as keys and the rows id's as values.
    """
    classifier = {getattr(instance, classifier): instance.id
                  for instance
                  in session_.query(table_class).order_by(table_class.id)}

    return classifier


def get_data_dict(n_pages: int = SNIPPET_PAGES) -> None:
    """ Prints the scraped data to the screen. If save_file will also save the information to a file
    :param n_pages: int, number of pages.
    """
    page_url = START_PAGE
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
    for dict_keys in (d.keys() for d in list_of_dicts):
        if name in dict_keys:
            return True
    return False


def is_email(string):
    """

    :param string:
    :return:
    """
    return '@' in string


def get_package_data(data_dict: dict):
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
        if 'stars' in a_dict:

            start_dict['github_stars'] = a_dict.get('stars')
            start_dict['github_forks'] = a_dict.get('forks')
            start_dict['github_open_issues'] = a_dict.get('open_issues')

        if 'author' in a_dict:
            author = a_dict.get('author')
            if author is None:
                continue
            else:
                author = a_dict.get('author')[0]  # list of 1 tuple
                start_dict['author'] = author[0]  # name
                start_dict['author_info'] = author[1]  # info
            if 'stars' and 'author' in a_dict:
                break
    return start_dict


def get_maintainers(data_dict: dict):

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


def create_new_maintainer(maintainer_dict: dict, session_: Session, package):
    """
    Adds new Person to the 'Person' table only if the new Person is not already in the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param maintainer_dict: A dict of the person data.
    :param session_: sqlalchemy.orm.session.Session.
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
        # session_.flush()


def create_new_environments(data_dict, package, session_=session):
    # environment_list = []

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
                   # session_.flush()
    #                 environment_list.append(Environment(environment=environment))
    # return environment_list


def create_new_programming_languages(data_dict, package, session_=session):
    # programming_language_list = []

    data = data_dict.values()
    for a_dict in data:
        programming_languages = a_dict.get('programming_language')
        if programming_languages:
            for programming_language in programming_languages:
                programming_languages_in_db = session_.query(ProgrammingLanguage).filter(
                    ProgrammingLanguage.programming_language == programming_language).first()
                if programming_languages_in_db:
                    package.package_programming_language.append(programming_languages_in_db)
                    # programming_language_list.append(ProgrammingLanguage(id=db_programming_languages[programming_language]))
                else:
                    package.package_programming_language.append(
                        ProgrammingLanguage(programming_language=programming_language))
                    # session_.flush()
#     return programming_language_list


def create_new_operating_systems(data_dict, package, session_=session):
    # operating_system_list = []

    data = data_dict.values()
    for a_dict in data:
        operating_systems = a_dict.get('operating_system')
        if operating_systems:
            for operating_system in operating_systems:
                operating_systems_in_db = session_.query(OperatingSystem).filter(
                    OperatingSystem.operating_system == operating_system).first()
                if operating_systems_in_db:
                    # operating_system_list.append(OperatingSystem(id=db_operating_systems[operating_system]))
                    package.package_operating_system.append(operating_systems_in_db)
                else:
                    # operating_system_list.append(OperatingSystem(operating_system=operating_system))
                    package.package_operating_system.append(OperatingSystem(operating_system=operating_system))
                    # session_.flush()
    # return operating_system_list


def create_new_intended_audiences(data_dict, package, session_=session):
    # intended_audience_list = []

    data = data_dict.values()
    for a_dict in data:
        intended_audiences = a_dict.get('intended_audience')
        if intended_audiences:
            for intended_audience in intended_audiences:
                intended_audiences_in_db = session_.query(IntendedAudience).filter(
                    IntendedAudience.intended_audience == intended_audience).first()
                if intended_audiences_in_db:
                    package.package_intended_audience.append(intended_audiences_in_db)
                    # intended_audience_list.append(IntendedAudience(id=db_intended_audiences[intended_audience]))
                else:
                    package.package_intended_audience.append(IntendedAudience(intended_audience=intended_audience))
                    # intended_audience_list.append(IntendedAudience(intended_audience=intended_audience))
    # return intended_audience_list


def create_new_frameworks(data_dict, package, session_=session):
    framework_list = []

    data = data_dict.values()
    for a_dict in data:
        frameworks = a_dict.get('framework')
        if frameworks:
            for framework in frameworks:
                framework_in_db = session_.query(Framework).filter(Framework.framework == framework).first()
                if framework_in_db:
                    package.package_framework.append(framework_in_db)
                    # framework_list.append(Framework(id=db_frameworks[framework]))
                else:
                    package.package_framework.append(Framework(framework=framework))
                    # framework_list.append(Framework(framework=framework))
    # return framework_list


def create_new_topics(data_dict, package, session_=session):
    # topic_list = []

    data = data_dict.values()
    for a_dict in data:
        topics = a_dict.get('topic')
        if topics:
            for topic in topics:
                topic_in_db = session_.query(Topic).filter(Topic.topic == topic).first()
                if topic_in_db:
                    package.package_topic.append(topic_in_db)
                    # topic_list.append(Topic(id=db_topics[topic]))
                else:
                    package.package_topic.append(Topic(topic=topic))
                    # topic_list.append(Topic(topic=topic))
    # return topic_list


def create_new_natural_languages(data_dict, package, session_=session):
    # natural_language_list = []

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
    # return natural_language_list


for data_dict in get_data_dict(1):
    print(data_dict)

    package_data = get_package_data(data_dict)
    if not package_data:
        continue
    package_name = package_data.get('name')
    package_in_db = session.query(Package).filter(Package.name == package_name).first()
    if package_in_db:
        if package_data.get('version') == package_in_db.version:
            continue
        else:
            continue  # todo - add update to existing packages with updated versions or dates
            # session.query(Package).filter(Package.name == package_name).update(**package_data)
            # package = package_in_db
    else:
        package = Package(**package_data)  # parent table
    # add maintainers
    maintainers_list = get_maintainers(data_dict)
    for maintainer_dict in maintainers_list:
        if maintainer_dict:
            create_new_maintainer(maintainer_dict, session, package)
    #        maintainer_record = create_new_maintainer(maintainer_dict, session)
    #
    #         package.package_maintainer.append(maintainer_record)
    # add programming_language
    create_new_programming_languages(data_dict, package)
    # for programming_language in programming_languages_list:
    #     package.package_programming_language.append(programming_language)
    # add natural_language
    create_new_natural_languages(data_dict, package)
    # for natural_language in natural_languages_list:
    #     package.package_natural_language.append(natural_language)
    # add operating_system
    create_new_operating_systems(data_dict, package)
    # for operating_system in operating_systems_list:
    #     package.package_operating_system.append(operating_system)
    # add intended_audience
    create_new_intended_audiences(data_dict, package)
    # for intended_audience in intended_audiences_list:
    #     package.package_intended_audience.append(intended_audience)
    # add framework
    create_new_frameworks(data_dict, package)
    # for framework in frameworks_list:
    #     package.package_framework.append(framework)
    # add environment
    create_new_environments(data_dict, package)
    # for environment in environments_list:
    #     package.package_environment.append(environment)
    # add topic
    create_new_topics(data_dict, package)
    # for topic in topics_list:
    #     package.package_topic.append(topic)

    session.add(package)
    # session.flush()
    session.commit()
    #
    #
    # print(data_dict)
    # print(get_person_data(data_dict))
    # print('-' * 10)
    # print(get_package_data(data_dict))
    # print('-' * 100)

    # At the end:



#