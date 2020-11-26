from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from db_config import DB_USER, DB_PASSWORD, DB_SERVER, DB_NAME
from create_db import Topic, Environment, Framework, IntendedAudience, NaturalLanguage, OperatingSystem, \
    ProgrammingLanguage
from scrap_package_page import make_classifier_key  # Todo move this function to the classifier file
from pypi_classifiers import get_all_classifiers
from config import DB

engine = create_engine(DB, echo=True)
Session = sessionmaker(bind=engine)


classifiers = {make_classifier_key(key): value for key, value in get_all_classifiers().items()}


# create a Session
session = Session()

session.add_all([Environment(environment=env) for env in classifiers['environment']])
session.add_all([Topic(topic=top) for top in classifiers['topic']])
session.add_all([Environment(environment=env) for env in classifiers['environment']])
session.add_all([Framework(framework=frame) for frame in classifiers['framework']])
session.add_all([IntendedAudience(intended_audience=audience) for audience in classifiers['intended_audience']])
session.add_all([NaturalLanguage(natural_language=nlan) for nlan in classifiers['natural_language']])
session.add_all([OperatingSystem(operating_system=os) for os in classifiers['operating_system']])
session.add_all([ProgrammingLanguage(programming_language=plan) for plan in classifiers['programming_language']])


session.commit()

