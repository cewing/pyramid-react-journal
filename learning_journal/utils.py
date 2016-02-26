# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy import engine_from_config


def create_session(settings):
    from sqlalchemy.orm import sessionmaker
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session = sessionmaker(bind=engine)
    return Session()
