"""The application's model objects"""
import transaction
import logging

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from fa.jquery.utils import HTML, Color, Slider
from datetime import datetime

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    text = Column(HTML)
    publication_date = Column(Date, default=datetime.now)


class Widgets(Base):
    __tablename__ = 'widgets'

    id = Column(Integer, primary_key=True)
    autocomplete = Column(Unicode)
    slider = Column(Slider, default=0)
    color = Column(Color)
    date = Column(Date)
    date_time = Column(DateTime, default=datetime.now)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group")

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    permission_id = Column(Integer, ForeignKey('permissions.id'))
    permissions = relationship("Permission")

    def __unicode__(self):
        return self.name

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)

    def __unicode__(self):
        return self.name

def populate():
    import random
    session = DBSession()

    for i, name in enumerate(['Read', 'Write']):
        o = Permission()
        o.name = name
        session.add(o)
        p = o
    transaction.commit()

    for i, name in enumerate(['Admins', 'Users']):
        o = Group()
        o.name = name
        o.permission = p
        session.add(o)
        g = o
    transaction.commit()

    for i, name in enumerate(['John', 'Jack', 'Daniel']):
        o = User()
        o.name = name
        o.group = g
        session.add(o)


    for i in range(50):
        article = Article(id=i,
                title='Article %s' % i,
                text='''Heading
=====================

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent consectetur
imperdiet porta. Pellentesque habitant morbi tristique senectus et netus et
malesuada fames ac turpis egestas. Proin sollicitudin, mi sit amet blandit
dignissim, lacus ante sagittis est, in congue lectus nulla non urna. Nunc a
justo ut lacus laoreet facilisis. Nullam blandit posuere mauris semper
pellentesque. Sed leo neque, vulputate sed pharetra vel, rhoncus at nisl.
Aenean eget nibh turpis. Quisque semper lacus sodales libero dictum pretium.
Phasellus euismod, odio sit amet vehicula pharetra, nunc diam imperdiet dui,
non malesuada neque erat ac augue. Sed elit ipsum, placerat vitae accumsan
quis, tempor in tellus. Vestibulum tempus consequat libero, sit amet
pellentesque lacus interdum in. Vestibulum in nunc at nulla ultrices laoreet.

* Morbi id orci augue, porta malesuada mi.
* Proin rhoncus tellus non orci iaculis pretium.
* Praesent aliquet commodo urna, vitae laoreet arcu porttitor ut.
* Nullam sollicitudin blandit risus, eu luctus nisl scelerisque eget.


Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent consectetur
imperdiet porta. Pellentesque habitant morbi tristique senectus et netus et
malesuada fames ac turpis egestas. Proin sollicitudin, mi sit amet blandit
dignissim, lacus ante sagittis est, in congue lectus nulla non urna. Nunc a
justo ut lacus laoreet facilisis. Nullam blandit posuere mauris semper
pellentesque. Sed leo neque, vulputate sed pharetra vel, rhoncus at nisl.
Aenean eget nibh turpis. Quisque semper lacus sodales libero dictum pretium.
Phasellus euismod, odio sit amet vehicula pharetra, nunc diam imperdiet dui,
non malesuada neque erat ac augue. Sed elit ipsum, placerat vitae accumsan
quis, tempor in tellus. Vestibulum tempus consequat libero, sit amet
pellentesque lacus interdum in. Vestibulum in nunc at nulla ultrices laoreet.
''',
            publication_date = datetime.utcnow())
        session.add(article)

    for i in range(100):
        widgets = Widgets(id=i,
                autocomplete=random.choice(['%sanux' % s for s in 'BCDFGHJKLMNP']+['']),
                color = random.choice(["#EEEEEE", "#FFFF88", "#FF7400", "#CDEB8B", "#6BBA70"]),
                slider = random.choice(range(0, 100, 10)),
                )
        session.add(widgets)
    transaction.commit()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError, e:
        DBSession.rollback()
