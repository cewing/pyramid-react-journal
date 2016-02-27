from __future__ import unicode_literals
import json
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.security import remember, forget
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .forms import EntryUpdateForm, EntryCreateForm
from .models import (
    DBSession,
    User,
    Entry
    )


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    authenticated = request.authenticated_userid
    page = int(request.params.get('page', 1))
    user = {}
    paginator = []
    pagination = ''
    if authenticated:
        paginator = Entry.get_paginator(request, page=page)
        user = request.user.to_json()
        pagination = paginator.pager(
            link_attr={'class': 'pagerItem link'},
            curpage_attr={'class': 'pagerItem'},
            dotdot_attr={'class': 'pagerItem'},
        )
    def jsonify_entry(entry, request=request):
        entry_json = entry.to_json()
        entry_json['url'] = request.route_url('entry', id=entry.id)
        return entry_json

    entries = [e for e in paginator]
    entries = list(map(jsonify_entry, entries))

    data = {
        'react_component': 'LJEntryList',
        'react_props': json.dumps({
            'user': user,
            'entries': entries,
            'pagination': pagination
        })
    }
    return data


@view_config(route_name='about', renderer='templates/about.jinja2')
def about_view(request):
    return {}


@view_config(route_name='entry', renderer='templates/entry.jinja2')
def entry_view(request):
    id = int(request.matchdict.get('id', -1))
    entry = Entry.by_id(id)
    if entry is None:
        raise HTTPNotFound()
    entry_json = entry.to_json()
    entry_json['actions'] = {}
    if entry.is_owned_by(request.user):
        entry_json['actions']['edit'] = request.route_url('edit', id=entry.id)
        entry_json['actions']['delete'] = request.route_url('delete', id=entry.id)
    data = {
        'react_component': 'LJEntry',
        'react_props': json.dumps({
            'entry': entry_json,
            'user': request.user.to_json(),
        })
    }
    return data


@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit_view(request):
    id = int(request.matchdict.get('id', -1))
    entry = Entry.by_id(id)
    # 404 if no entry
    if entry is None:
        raise HTTPNotFound()
    # 403 if not my entry
    if not entry.is_owned_by(request.user):
        raise HTTPForbidden()

    form = EntryUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        return HTTPFound(location=request.route_url('entry', id=entry.id))
    return {
        'form': form,
        'url': request.current_route_url(),
        'cancel': request.route_url('entry', id=entry.id)
    }


@view_config(route_name='create', renderer='templates/create.jinja2')
def create_view(request):
    if not request.user:
        return HTTPForbidden()

    entry = Entry()
    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        entry.author = request.user
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'cancel': request.route_url('home')}


@view_config(route_name='delete', renderer='string')
def delete_view(request):
    id = int(request.matchdict.get('id', -1))
    entry = Entry.by_id(id)
    if entry is None:
        return HTTPFound(location=request.route_url('home'))
    if not entry.is_owned_by(request.user):
        raise HTTPForbidden()

    DBSession.delete(entry)
    return HTTPFound(location=request.route_url('home'))


@view_config(
    context='velruse.AuthenticationComplete',
    renderer='json'
)
def login_complete_view(context, request):
    profile = context.profile
    display_name = profile['displayName']
    username = profile['preferredUsername']
    user = msg = None
    if username in request.approved:
        try:
            user = User.by_username(username)
        except NoResultFound:
            user = User.create(display_name, username)
            msg = "You have been added to the site.  Welcome!"
        except MultipleResultsFound:
            msg = 'Unable to identify a unique registered user'
            level = 'danger'
    else:
        msg = ("You are not an approved member of this site. If you believe "
               "this is an error, please contact your instructor or TA for "
               "assistance")
        level = 'warning'

    if msg:
        request.session.flash(msg, level)

    if user:
        headers = remember(request, user.username)
    else:
        headers = forget(request)

    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
