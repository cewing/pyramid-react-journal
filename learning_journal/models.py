from __future__ import unicode_literals
import datetime
import markdown
from paginate_sqlalchemy import SqlalchemyOrmPage
from pyramid.security import Allow, Everyone
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime,
    ForeignKey,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )
from sqlalchemy.dialects.postgresql import UUID
import uuid

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    display_name = Column(Unicode(128), nullable=False)
    username = Column(Unicode(128), nullable=False)
    course_id = Column(Unicode(32), nullable=False, default=u"sea401d2")
    key = Column(UUID(as_uuid=True))

    def __json__(self, request):
        return {
            'username': self.username,
            'display_name': self.display_name,
            'id': self.id,
            'course_id': self.course_id.split('|')
        }

    def to_json(self, request=None):
        return self.__json__(request)

    @property
    def api_key(self):
        if self.key is None:
            self.key = uuid.uuid4()
        return self.key

    @property
    def allowed_courses(self):
        return set(self.course_id.split('|'))


    @classmethod
    def valid_api_key(cls, key, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.key == key).count() > 0

    @classmethod
    def by_api_key(cls, key, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.key == key).one()

    @classmethod
    def by_username(cls, username, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(User.username == username).one()

    @classmethod
    def by_id(cls, id, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).get(id)

    @classmethod
    def create(cls, display_name, username, session=None):
        if session is None:
            session = DBSession
        new_user = cls(display_name=display_name, username=username)
        session.add(new_user)
        return new_user


Index('user_username', User.username, unique=True, mysql_length=255)


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Unicode(127), nullable=False)
    text = Column(UnicodeText, nullable=False)
    created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="entries")

    # object level security
    @property
    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, 'g:users', 'read'),
            (Allow, 'g:users', 'create'),
            (Allow, self.author.username, 'edit'),
            (Allow, self.author.username, 'delete'),
        ]

    # traversal
    @property
    def __name__(self):
        return self.id

    def __json__(self, request):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'markdown': self.markdown,
            'created': self.created.isoformat(),
            'author': self.author.to_json(request),
        }

    def to_json(self, request=None):
        return self.__json__(request)

    def is_owned_by(self, user):
        if user is None:
            return False
        return user.id == self.author.id

    @property
    def markdown(self):
        ext = "codehilite(linenums=False, pygments_style=colorful)"
        rendered = markdown.markdown(
            self.text, extensions=[ext, 'fenced_code']
        )
        return rendered

    @classmethod
    def write(cls, title=None, text=None, session=None):
        if session is None:
            session = DBSession
        instance = cls(title=title, text=text)
        session.add(instance)
        return instance

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).order_by(cls.created.desc())

    @classmethod
    def by_id(cls, id, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).get(id)

    @classmethod
    def by_author(cls, author, session=None):
        if session is None:
            session = DBSession
        all_entries = cls.all()
        return all_entries.filter(cls.author == author)

    @classmethod
    def get_paginator(cls, request, page=1):
        query = cls.all()
        query_params = request.GET.mixed()

        def url_maker(link_page):
            # replace page param with values generated by paginator
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return SqlalchemyOrmPage(
            query,
            page,
            items_per_page=10,
            url_maker=url_maker,
        )


User.entries = relationship(
    "Entry", order_by=Entry.created, back_populates="author"
)
