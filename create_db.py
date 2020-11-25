from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from db_config import DB_USER, DB_PASSWORD, DB_SERVER, DB_NAME

# If have not created a database on the server then you can connect directly to the
# server and execute the following:
# engine.execute("CREATE DATABASE pypi")
# engine.execute("USE pypi")

Base = declarative_base()


class Package(Base):
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    version = Column(String(50), nullable=False)
    description = Column(String(255))
    package_license = Column(String(128))
    release_date = Column(DateTime)
    github_stars = Column(Integer)
    github_forks = Column(Integer)
    github_open_issues = Column(Integer)

    package_operating_system = relationship('PackageOperatingSystem', back_populates='package')
    package_programming_language = relationship('PackageProgrammingLanguage', back_populates='package')
    package_topic = relationship("PackageTopic", back_populates='package')
    package_environment = relationship('PackageEnvironment', back_populates='package')
    package_framework = relationship('PackageFramework', back_populates='package')
    package_intended_audience = relationship('PackageIntendedAudience', back_populates='package')
    package_maintainer = relationship('Maintainer', back_populates='package')
    package_author = relationship('Author', back_populates='package')
    package_natural_language = relationship('PackageNaturalLanguage', back_populates='package')

    __table_args__ = (UniqueConstraint('name', 'version', name='_name_version_uc'),)


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    email = Column(String(100))
    pypi_page = Column(String(128))
    package_maintainer = relationship('Maintainer', back_populates='person')
    package_author = relationship('Author', back_populates='person')


class Maintainer(Base):
    __tablename__ = 'package_maintainer'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    package_id = Column(Integer, ForeignKey('package.id'))
    person = relationship('Person', back_populates='package_maintainer')
    package = relationship('Package', back_populates='package_maintainer')


class Author(Base):
    __tablename__ = 'package_author'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    package_id = Column(Integer, ForeignKey('package.id'))
    person = relationship('Person', back_populates='package_author')
    package = relationship('Package', back_populates='package_author')


class NaturalLanguage(Base):
    __tablename__ = 'natural_language'
    id = Column(Integer, primary_key=True)
    natural_language = Column(String(64), nullable=False, unique=True)
    package_natural_language = relationship('PackageNaturalLanguage', back_populates='natural_language')


class PackageNaturalLanguage(Base):
    __tablename__ = 'package_natural_language'
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    natural_language_id = Column(Integer, ForeignKey('natural_language.id'))
    natural_language = relationship('NaturalLanguage', back_populates='package_natural_language')
    package = relationship('Package', back_populates='package_natural_language')


class Framework(Base):
    __tablename__ = 'framework'
    id = Column(Integer, primary_key=True)
    framework = Column(String(64), nullable=False, unique=True)
    package_framework = relationship('PackageFramework', back_populates='framework')


class PackageFramework(Base):
    __tablename__ = 'package_framework'
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    framework_id = Column(Integer, ForeignKey('framework.id'))
    framework = relationship('Framework', back_populates='package_framework')
    package = relationship('Package', back_populates='package_framework')


class Environment(Base):
    __tablename__ = 'environment'
    id = Column(Integer, primary_key=True)
    environment = Column(String(64), nullable=False, unique=True)
    package_environment = relationship('PackageEnvironment', back_populates='environment')


class PackageEnvironment(Base):
    __tablename__ = 'package_environment'
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    environment_id = Column(Integer, ForeignKey('environment.id'))
    package = relationship('Package', back_populates='package_environment')
    environment = relationship('Environment', back_populates='package_environment')


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    topic = Column(String(128), nullable=False, unique=True)
    package_topic = relationship('PackageTopic', back_populates='topic')


class PackageTopic(Base):
    __tablename__ = 'package_topic'
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic = relationship('Topic', back_populates='package_topic')
    package = relationship('Package', back_populates='package_topic')


class ProgrammingLanguage(Base):
    __tablename__ = 'programming_language'
    id = Column(Integer, primary_key=True)
    programming_language = Column(String(64), nullable=False, unique=True)
    package_programming_language = relationship('PackageProgrammingLanguage', back_populates='programming_language')


class PackageProgrammingLanguage(Base):
    __tablename__ = 'package_programming_language'
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    programming_language_id = Column(Integer, ForeignKey('programming_language.id'))
    package = relationship('Package', back_populates='package_programming_language')
    programming_language = relationship('ProgrammingLanguage', back_populates='package_programming_language')


class OperatingSystem(Base):
    __tablename__ = 'operating_system'
    id = Column(Integer, primary_key=True)
    operating_system = Column(String(64), nullable=False, unique=True)
    package_operating_system = relationship('PackageOperatingSystem', back_populates='operating_system')


class PackageOperatingSystem(Base):
    __tablename__ = 'package_operating_system'
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    operating_system_id = Column(Integer, ForeignKey('operating_system.id'))
    package = relationship('Package', back_populates='package_operating_system')
    operating_system = relationship('OperatingSystem', back_populates='package_operating_system')


class IntendedAudience(Base):
    __tablename__ = 'intended_audience'
    id = Column(Integer, primary_key=True)
    intended_audience = Column(String(128), nullable=False, unique=True)
    package_intended_audience = relationship('PackageIntendedAudience', back_populates='intended_audience')


class PackageIntendedAudience(Base):
    __tablename__ = 'package_intended_audience'
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    intended_audience_id = Column(Integer, ForeignKey('intended_audience.id'))
    package = relationship('Package', back_populates='package_intended_audience')
    intended_audience = relationship('IntendedAudience', back_populates='package_intended_audience')


if __name__ == '__main__':
    DB = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'
    engine = create_engine(DB, echo=True)

    DBSession = sessionmaker()
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
