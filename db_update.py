from sqlalchemy.ext.declarative import declarative_base
from scrap_package_page import *


Base = declarative_base()

s = session()
for name, job in dct.iteritems():
    np = Person(name=name, job=job)
    s.add(np)
    s.commit()
