from db.create_db import Package, Maintainer, ProgrammingLanguage, NaturalLanguage, OperatingSystem,\
    IntendedAudience, Framework, Environment, Topic, GithubInfo, get_db_info
import sqlalchemy.orm.session as session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging

logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)


def create_db_session() -> session:
    """Creating a Database sqlalchemy session"""
    db_name, db_server, db_user, db_password = get_db_info()
    db_url = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_server}/{db_name}'
    engine = create_engine(db_url, echo_pool=True, logging_name='sqlalchemy.engine')
    return sessionmaker(bind=engine)()


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
    :param string: string
    :return: True or False
    """
    return '@' in string


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


def create_new_maintainer(maintainer_dict: dict, session_: session, package: Package) -> None:
    """Adds maintainers to the package package_maintainer. if the maintainer is not
    already in the database in the maintainer table then the code adds the maintainer to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param maintainer_dict: A dict of the maintainer data.
    :param session_: sqlalchemy.orm.session.
    :param package: A package object (sqlalchemy table)
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


def create_new_environments(data_dict: dict, package: Package, session_: session) -> None:
    """Adds environments to the package package_environment. if the environment is not
    already in the database in the environment table then the code adds the environment to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package: A package object (sqlalchemy table)
    :param session_: sqlalchemy.orm.session.
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


def create_new_programming_languages(data_dict: dict, package: Package, session_: session) -> None:
    """Adds programming languages to the package package_programming_language. if the programming language is not
    already in the database in the programming_language table then the code adds the programming language to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package: A package object (sqlalchemy table)
    :param session_: sqlalchemy.orm.session.
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


def create_new_operating_systems(data_dict: dict, package: Package, session_: session) -> None:
    """Adds operating systems to the package package_operating_system. if the operating system is not
    already in the database in the operating_system table then the code adds the operating system to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package: A package object (sqlalchemy table)
    :param session_: sqlalchemy.orm.session.
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


def create_new_intended_audiences(data_dict: dict, package: Package, session_: session) -> None:
    """Adds intended audiences to the package package_intended_audience. if the intended audience is not
    already in the database in the intended_audience table then the code adds the intended audience to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package: A package object (sqlalchemy table)
    :param session_: sqlalchemy.orm.session.
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


def create_new_frameworks(data_dict: dict, package: Package, session_: session) -> None:
    """Adds frameworks to the package package_framework. if the framework is not
    already in the database in the framework table then the code adds the framework to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package: A package object (sqlalchemy table)
    :param session_: sqlalchemy.orm.session.
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


def create_new_topics(data_dict: dict, package: Package, session_: session) -> None:
    """Adds topics to the package package_topic. if the topic is not
    already in the database in the topic table then the code adds the topic to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package: A package object (sqlalchemy table)
    :param session_: sqlalchemy.orm.session.
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


def create_new_natural_languages(data_dict: dict, package: Package, session_: session) -> None:
    """Adds natural languages to the package package_natural_language. if the natural language is not
    already in the database in the natural_language table then the code adds the natural languages to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package: A package object (sqlalchemy table)
    :param session_: sqlalchemy.orm.session.
    """
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


def create_new_github_info(data_dict: dict, package: Package, session_: session) -> None:
    """Adds github_info to the package package github_info. if the github_info is not
    already in the database in the github_info table then the code adds the github_info to the table.
    Dose NOT COMMIT to the database but only adds to the session.
    :param data_dict: Dict with package info (that is returned from the scraper).
    :param package: A package object (sqlalchemy table)
    :param session_: sqlalchemy.orm.session.
    """
    data = data_dict.values()
    for a_dict in data:
        github_url = a_dict.get('github_url')
        if github_url:

            github_url_in_db = session_.query(GithubInfo).filter(
                GithubInfo.github_url == github_url).first()
            if github_url_in_db:
                package.github_info = github_url_in_db
            else:
                package.github_info = GithubInfo(github_url=github_url,
                                                 github_stars=a_dict.get('github_stars'),
                                                 github_forks=a_dict.get('github_forks'),
                                                 github_open_issues=a_dict.get('github_open_issues'),
                                                 github_contributors=a_dict.get('github_contributors'))
