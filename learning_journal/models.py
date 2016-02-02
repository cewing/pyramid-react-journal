from __future__ import unicode_literals
import datetime

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

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    display_name = Column(Unicode(128), nullable=False)
    username = Column(Unicode(128), nullable=False)

    @classmethod
    def by_username(cls, username, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(User.username == username).one()

    @classmethod
    def create(cls, display_name, username, session=None):
        if session is None:
            session = DBSession
        new_user = cls(display_name=display_name, username=username)
        session.add(new_user)
        return new_user

    def __json__(self):
        return {
            'username': self.username,
            'display_name': self.display_name,
            'id': self.id,
        }


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
        return session.query(cls).order_by(cls.created.desc()).all()


User.entries = relationship(
    "Entry", order_by=Entry.created, back_populates="author"
)
