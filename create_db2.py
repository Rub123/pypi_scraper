from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from db_config import DB_USER, DB_PASSWORD, DB_SERVER, DB_NAME
import datetime

# If have not created a database on the server then you can connect directly to the
# server and execute the following:
# engine.execute("CREATE DATABASE pypi")
# engine.execute("USE pypi")

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
    github_stars = Column(Integer)
    github_forks = Column(Integer)
    github_open_issues = Column(Integer)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

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


class Maintainer(Base):
    __tablename__ = 'maintainer'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(100))
    pypi_page = Column(String(128))
    maintainer_packages = relationship('Package',
                                       secondary=package_maintainer_association,
                                       back_populates='package_maintainer')


class NaturalLanguage(Base):
    __tablename__ = 'natural_language'
    id = Column(Integer, primary_key=True)
    natural_language = Column(String(64), unique=True)
    natural_language_packages = relationship('Package',
                                             secondary=package_natural_language_association,
                                             back_populates='package_natural_language')


class Framework(Base):
    __tablename__ = 'framework'
    id = Column(Integer, primary_key=True)
    framework = Column(String(64), unique=True)
    framework_packages = relationship('Package',
                                      secondary=package_framework_association,
                                      back_populates='package_framework')


class Environment(Base):
    __tablename__ = 'environment'
    id = Column(Integer, primary_key=True)
    environment = Column(String(64), unique=True)
    environment_packages = relationship('Package',
                                        secondary=package_environment_association,
                                        back_populates='package_environment')


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    topic = Column(String(128), unique=True)
    topic_packages = relationship('Package',
                                  secondary=package_topic_association,
                                  back_populates='package_topic')


class ProgrammingLanguage(Base):
    __tablename__ = 'programming_language'
    id = Column(Integer, primary_key=True)
    programming_language = Column(String(64), unique=True)
    programming_language_packages = relationship('Package',
                                                 secondary=package_programming_language_association,
                                                 back_populates='package_programming_language')


class OperatingSystem(Base):
    __tablename__ = 'operating_system'
    id = Column(Integer, primary_key=True)
    operating_system = Column(String(128), unique=True)
    operating_system_packages = relationship('Package',
                                             secondary=package_operating_system_association,
                                             back_populates='package_operating_system')


class IntendedAudience(Base):
    __tablename__ = 'intended_audience'
    id = Column(Integer, primary_key=True)
    intended_audience = Column(String(128), unique=True)
    intended_audience_packages = relationship('Package',
                                              secondary=package_intended_audience_association,
                                              back_populates='package_intended_audience')


if __name__ == '__main__':
    DB = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'
    engine = create_engine(DB, echo=True)

    DBSession = sessionmaker()
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
