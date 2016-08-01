from __future__ import unicode_literals
import json
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.view import (
    view_config,
    notfound_view_config,
    forbidden_view_config
    )
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .forms import EntryUpdateForm, EntryCreateForm
from .models import (
    DBSession,
    User,
    Entry
    )


# Basic applicaion views

@view_config(
    route_name='home', renderer='templates/home.jinja2', permission='view'
)
def home_view(request):
    authenticated = request.authenticated_userid
    page = int(request.params.get('page', 1))
    user_data = {}
    paginator = []
    pagination = ''
    if authenticated:
        # the get_paginator method handles filtering for users' allowed courses
        paginator = Entry.get_paginator(request, page=page)
        user_data = request.user.to_json()
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
            'user': user_data,
            'entries': entries,
            'pagination': pagination
        })
    }
    return data


@view_config(route_name='mine', renderer="json", permission='view')
def mine_view(request):
    if not request.user:
        return HTTPForbidden()
    my_entries = Entry.by_author(request.user)
    return {'entries': my_entries.all()}


@view_config(
    route_name='about', renderer='templates/about.jinja2', permission='view'
)
def about_view(request):
    return {}


@view_config(
    route_name='apikey', renderer='templates/key.jinja2', permission='read'
)
def key_view(request):
    if not request.user:
        return HTTPForbidden
    return {'key': request.user.api_key}


# Views to manage entries

@view_config(route_name="export", renderer='json', valid_api_key=True)
def api_export_view(request):
    key = request.params['apikey']
    try:
        user = User.by_api_key(key)
    except (NoResultFound, MultipleResultsFound):
        result = {'error': 'INVALID API KEY'}
    else:
        result = Entry.by_author(user).all()
    return result

@view_config(
    route_name='create', renderer='templates/create.jinja2', permission='create'
)
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


@view_config(
    route_name='entry', renderer='templates/entry.jinja2', permission='read'
)
def entry_view(context, request):
    entry_json = context.to_json()
    entry_json['actions'] = actions = {}
    # use permissions to control access to edit and delete actions
    for action in ['edit', 'delete']:
        if request.has_permission(action):
            actions[action] = request.route_url(action, id=context.id)

    data = {
        'react_component': 'LJEntry',
        'react_props': json.dumps({
            'entry': entry_json,
            'user': request.user.to_json(),
        })
    }
    return data


@view_config(
    route_name='edit', renderer='templates/edit.jinja2', permission='edit'
)
def edit_view(context, request):
    view_url = request.route_url('entry', id=context.id)
    form = EntryUpdateForm(request.POST, context)
    if request.method == 'POST' and form.validate():
        form.populate_obj(context)
        return HTTPFound(location=view_url)
    return {
        'form': form,
        'url': request.current_route_url(),
        'cancel': view_url
    }


@view_config(route_name='delete', renderer='string', permission='delete')
def delete_view(context, request):
    if context is not None:
        DBSession.delete(context)

    return HTTPFound(location=request.route_url('home'))


# Authentication views

@view_config(
    context='velruse.AuthenticationComplete',
    renderer='json'
)
def login_complete_view(context, request):
    profile = context.profile
    display_name = profile['displayName']
    if display_name is None:
        display_name = ''
    username = profile['preferredUsername']
    user = msg = None
    if username.lower() in request.approved:
        try:
            user = User.by_username(username)
        except NoResultFound:
            user = User.create(display_name, username)
            msg = "You have been added to the site.  Welcome!"
            level = 'success'
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


# Error Views

@notfound_view_config(renderer='/templates/err.jinja2')
def notfound_view(context, request):
    data = {
        'title': 'Oooops!',
        'subtitle': 'We couldn\'t find what you are looking for',
        'explanation': 'Maybe it just doesn\'t exist?'
    }
    return data


@notfound_view_config(route_name='export')
def api_notfound(context, request):
    return Response(
        '{"error": "INVALID API KEY"}',
        status="404 Not Found",
        content_type="application/json",
        content_type_params={'charset': 'utf-8'}
    )


@forbidden_view_config(renderer='templates/err.jinja2')
def forbidden_view(context, request):
    data = {
        'title': 'Uh uh uh!',
        'subtitle': 'You aren\'t allowed to do that!',
        'explanation': ('What? You say you should be able to? Contact your '
                        'instructor or TA and see if they can help.')
    }
    return data
