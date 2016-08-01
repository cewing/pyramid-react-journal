# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import unauthenticated_userid
from sqlalchemy import engine_from_config
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .models import User

APPROVED = 'learning_journal.approved_usernames'
ADMINS = 'learning_journal.admins'
COURSES = 'learning_journal.course_ids'


def create_session(settings):
    from sqlalchemy.orm import sessionmaker
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session = sessionmaker(bind=engine)
    return Session()


def get_user(request):
    userid = unauthenticated_userid(request)
    try:
        user = User.by_username(userid)
    except (MultipleResultsFound, NoResultFound):
        user = None
    return user


def get_names(request, key):
    raw = request.registry.settings.get(key, '')
    fixed = map(str.lower, raw.split())
    return set(list(fixed))


def get_users(request, key):
    raw = request.registry.settings.get(key, '')
    # split on whitespace and strip to remove commas
    fixed = list(map(
        lambda x: x.strip(','),
        map(str.lower, raw.split())
    ))
    first = fixed[::2]
    second = fixed[1::2]
    return dict(zip(first, second))


def get_approved_users(request):
    return get_users(request, APPROVED)


def get_admin_users(request):
    return get_users(request, ADMINS)


def get_active_courses(request):
    user_courses = request.user.allowed_courses
    all_courses = get_names(request, COURSES)
    if 'all' not in user_courses:
        all_courses &= user_courses
    return all_courses
