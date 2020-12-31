import configparser
from pathlib import Path

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime

# If have not created a database on the server then you can connect directly to the
# server and execute the following:
# engine.execute("CREATE DATABASE pypi")
# engine.execute("USE pypi")


def get_db_info():
    """
    the function gets the user_name, server, db name and password to sql server fron ini file
    """
    config = configparser.ConfigParser()
    config.read(Path('db_config.ini').absolute())
    name = config['db']['db_name']
    server = config['db']['server']
    user = config['db']['user']
    password = config['db']['password']
    return name, server, user, password


Base = declarative_base()

package_operating_system_association = Table(
    'package_operating_system_association', Base.metadata,
    Column('package_id', Integer, ForeignKey('package.id')),
    Column('operating_system_id', Integer, ForeignKey('operating_system.id'))
)

package_natural_language_association = Table(
    'package_natural_language_association', Base.metadata,
    Column('package_id', Integer, ForeignKey('package.id')),
    Column('natural_language_id', Integer, ForeignKey('natural_language.id'))
)

package_framework_association = Table(
    'package_framework_association', Base.metadata,
    Column('package_id', Integer, ForeignKey('package.id')),
    Column('framework_id', Integer, ForeignKey('framework.id'))
)

package_environment_association = Table(
    'package_environment_association', Base.metadata,
    Column('package_id', Integer, ForeignKey('package.id')),
    Column('environment_id', Integer, ForeignKey('environment.id'))
)

package_topic_association = Table(
    'package_topic_association', Base.metadata,
    Column('package_id', Integer, ForeignKey('package.id')),
    Column('topic_id', Integer, ForeignKey('topic.id'))
)

package_programming_language_association = Table(
    'package_programming_language_association', Base.metadata,
    Column('package_id', Integer, ForeignKey('package.id')),
    Column('programming_language_id', Integer, ForeignKey('programming_language.id'))
)

package_intended_audience_association = Table(
    'package_intended_audience_association', Base.metadata,
    Column('package_id', Integer, ForeignKey('package.id')),
    Column('intended_audience_id', Integer, ForeignKey('intended_audience.id'))
)

package_maintainer_association = Table(
    'package_maintainer_association', Base.metadata,
    Column('package_id', Integer, ForeignKey('package.id')),
    Column('maintainer_id', Integer, ForeignKey('maintainer.id'))
)


class Package(Base):
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    version = Column(String(255))
    author = Column(String(255))
    author_info = Column(String(255))
    description = Column(String(600))
    package_license = Column(String(255))
    release_date = Column(DateTime)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Package(name='{self.name}', version={'self.version'}, release_date='{str(self.release_date)}')>"

    github_info = relationship('GithubInfo', uselist=False, back_populates='package')

    package_operating_system = relationship('OperatingSystem',
                                            secondary=package_operating_system_association,
                                            back_populates='operating_system_packages')

    package_programming_language = relationship('ProgrammingLanguage',
                                                secondary=package_programming_language_association,
                                                back_populates='programming_language_packages')

    package_topic = relationship("Topic",
                                 secondary=package_topic_association,
                                 back_populates='topic_packages')

    package_environment = relationship('Environment',
                                       secondary=package_environment_association,
                                       back_populates='environment_packages')

    package_framework = relationship('Framework',
                                     secondary=package_framework_association,
                                     back_populates='framework_packages')

    package_intended_audience = relationship('IntendedAudience',
                                             secondary=package_intended_audience_association,
                                             back_populates='intended_audience_packages')

    package_maintainer = relationship('Maintainer',
                                      secondary=package_maintainer_association,
                                      back_populates='maintainer_packages')

    package_natural_language = relationship('NaturalLanguage',
                                            secondary=package_natural_language_association,
                                            back_populates='natural_language_packages')


class GithubInfo(Base):
    __tablename__ = 'github_info'
    id = Column(Integer, primary_key=True)
    github_url = Column(String(255))
    github_stars = Column(Integer)
    github_forks = Column(Integer)
    github_open_issues = Column(Integer)
    github_contributors = Column(Integer)

    package_id = Column(Integer, ForeignKey('package.id'))
    package = relationship('Package', back_populates='github_info')


class Maintainer(Base):
    __tablename__ = 'maintainer'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(100))
    pypi_page = Column(String(128))
    maintainer_packages = relationship('Package',
                                       secondary=package_maintainer_association,
                                       back_populates='package_maintainer')

    def __repr__(self):
        return f"<Maintainer(name='{self.name}')>"


class NaturalLanguage(Base):
    __tablename__ = 'natural_language'
    id = Column(Integer, primary_key=True)
    natural_language = Column(String(64), unique=True)
    natural_language_packages = relationship('Package',
                                             secondary=package_natural_language_association,
                                             back_populates='package_natural_language')

    def __repr__(self):
        return f"<NaturalLanguage(natural_language='{self.natural_language}')>"


class Framework(Base):
    __tablename__ = 'framework'
    id = Column(Integer, primary_key=True)
    framework = Column(String(64), unique=True)
    framework_packages = relationship('Package',
                                      secondary=package_framework_association,
                                      back_populates='package_framework')

    def __repr__(self):
        return f"<Framework(framework='{self.framework}')>"


class Environment(Base):
    __tablename__ = 'environment'
    id = Column(Integer, primary_key=True)
    environment = Column(String(64), unique=True)
    environment_packages = relationship('Package',
                                        secondary=package_environment_association,
                                        back_populates='package_environment')

    def __repr__(self):
        return f"<Environment(environment='{self.environment}')>"


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    topic = Column(String(128), unique=True)
    topic_packages = relationship('Package',
                                  secondary=package_topic_association,
                                  back_populates='package_topic')

    def __repr__(self):
        return f"<Topic(topic='{self.topic}')>"


class ProgrammingLanguage(Base):
    __tablename__ = 'programming_language'
    id = Column(Integer, primary_key=True)
    programming_language = Column(String(64), unique=True)
    programming_language_packages = relationship('Package',
                                                 secondary=package_programming_language_association,
                                                 back_populates='package_programming_language')

    def __repr__(self):
        return f"<ProgrammingLanguage(programming_language='{self.programming_language}')>"


class OperatingSystem(Base):
    __tablename__ = 'operating_system'
    id = Column(Integer, primary_key=True)
    operating_system = Column(String(128), unique=True)
    operating_system_packages = relationship('Package',
                                             secondary=package_operating_system_association,
                                             back_populates='package_operating_system')

    def __repr__(self):
        return f"<OperatingSystem(operating_system='{self.operating_system}')>"


class IntendedAudience(Base):
    __tablename__ = 'intended_audience'
    id = Column(Integer, primary_key=True)
    intended_audience = Column(String(128), unique=True)
    intended_audience_packages = relationship('Package',
                                              secondary=package_intended_audience_association,
                                              back_populates='package_intended_audience')

    def __repr__(self):
        return f"<IntendedAudience(intended_audience='{self.intended_audience}')>"


if __name__ == '__main__':
    db_name, db_server, db_user, db_password = get_db_info()
    DB = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_server}'
    engine = create_engine(DB, echo=True)
    engine.execute(f"CREATE DATABASE {db_name}")
    engine.execute(f"USE {db_name}")
    DBSession = sessionmaker()
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
