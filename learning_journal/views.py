from __future__ import unicode_literals
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .models import (
    DBSession,
    User
    )


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    one = 'one'
    return {'one': one, 'project': 'learning_journal'}


@view_config(
    context='velruse.AuthenticationComplete',
    renderer='json'
)
def login_complete_view(context, request):
    profile = context.profile
    display_name = profile['displayName']
    username = profile['preferredUsername']
    try:
        user = User.by_username(username)
    except NoResultFound:
        user = User.create(display_name, username)
    except MultipleResultsFound:
        user = None

    if user:
        request.session['user'] = user.__json__()
        headers = remember(request, user.username)
    else:
        request.session.flash('Unable to identify a unique registered user')
        headers = forget(request)

    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
