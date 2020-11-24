from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from db_config import DB_USER, DB_PASSWORD, DB_SERVER, DB_NAME
from create_db import Topic, Environment, Framework, IntendedAudience, NaturalLanguage, OperatingSystem, \
    ProgrammingLanguage
from scrap_package_page import make_classifier_key  # Todo move this function to the classifier file
from pypi_classifiers import get_all_classifiers

# Base = declarative_base()
DB = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'

engine = create_engine(DB, echo=True)
Session = sessionmaker(bind=engine)


classifiers = {make_classifier_key(key): value for key, value in get_all_classifiers().items()}


# create a Session
session = Session()

session.add_all([Environment(environment=env) for env in classifiers['environment']])

session.commit()

