import os
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import (
    Configurator,
    ConfigurationError,
    )
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config
from velruse import login_url

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # inject the url from the environment
    settings['sqlalchemy.url'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://cewing:@localhost:5432/lj2'
    )
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)

    # github authentication configuration:
    config.include('velruse.providers.github')
    github_key = os.environ.get('LJ_GITHUB_KEY', None)
    github_secret = os.environ.get('LJ_GITHUB_SECRET', None)
    if not github_key and not github_secret:
        raise ConfigurationError(
            'Github Login requires LJ_GITHUB_SECRET and LJ_GITHUB_KEY set in the environment'
        )
    config.add_github_login(
        consumer_key=github_key,
        consumer_secret=github_secret,
        scope=settings.get(
            'velruse.providers.github.scope', 'user, public_repo'
        ),
    )
    # provide constructing the login url as a request method
    config.add_request_method(
        lambda req, svc='github': login_url(req, svc),
        name='login_url'
    )

    # session configuration
    session_secret = os.environ.get('LJ_SESSION_SECRET', 'itsaseekrit')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)

    # authn/authz configuration
    auth_secret = os.environ.get('LJ_AUTH_SECRET', 'itsaseekrit')
    authentication_policy=AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authentication_policy)
    authorization_policy=ACLAuthorizationPolicy()
    config.set_authorization_policy(authorization_policy)

    # templating configuration
    config.include('pyramid_jinja2')

    # view configuration
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
