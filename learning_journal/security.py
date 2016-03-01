# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone
from pyramid.security import ALL_PERMISSIONS

from .models import Entry


class DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'g:users', 'read'),
        (Allow, 'g:users', 'create'),
        (Allow, 'g:admins', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request


def groupfinder(userid, request):
    # this method is expected to return None if the userid is not "okay"
    groups = []
    if userid.lower() in request.approved:
        groups.append('g:users')
    if userid.lower() in request.admins:
        groups.append('g:admins')
    return groups or None


class EntryRoot(object):

    __name__ = 'entry'

    @property
    def __parent__(self):
        return DefaultRoot(self.request)

    def __init__(self, request):
        self.request = request

    def __getitem__(self, name):
        entry_obj = Entry.by_id(name)
        if entry_obj is None:
            raise KeyError(name)
        entry_obj.__parent__ = self
        return entry_obj