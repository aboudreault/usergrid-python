# -*- coding: utf-8 -*-

"""
usergrid.session
~~~~~~~~~~~~~~~

This module contains the usergrid sessions. A session handles how the
authentication and communication are done with a usergrid server.
"""

import re
import urllib

from .rest import RESTClient as rest
from .exceptions import (
    UsergridException,
    RESTError
)

class BaseSession(object):
    API_URL = 'api.usergrid.com'
    APP_NAME = 'sandbox'

    def __init__(self, org_name,
                 api_url=None,
                 app_name=None):
        """Initialize a BaseSession.

        :param org_name: the organization name of the session.
        :param api_url: (optional) the main url (host) of the usergrid server. Default to  'api.usergrid.com'.
        "param app_name: (optional) the application name of the session. Default to 'sandbox'.
        """

        self.api_url = api_url if api_url else self.API_URL
        self.app_name = app_name if app_name else self.APP_NAME
        self.org_name = org_name
        self.token = None

    def is_linked(self):
        """Return whether the UsergridSession has an access token attached."""
        return bool(self.token)

    def unlink(self):
        """Remove any attached access token from the UsergridSession."""
        self.token = None

    def build_path(self, target, params=None):
        """Build the url path components
        Returns the url path and parameters components.

        :param target: a target url (ie '/users').
        :param params: (optional) a dictionary or paramaters.
        """

        params = params or {}

        if params:
            return "/%s?%s" % (target, urllib.urlencode(params))
        else:
            return "/%s" % target

    def build_url(self, target, params=None):
        """Build an API URL.
        Returns the url for a specific request.

        :param target: a target url (ie. '/users').
        :param params: (optional) a dictionary or parameters.
        """

        url = "%s/%s/%s%s" % (
            self.api_url,
            self.org_name,
            self.app_name,
            self.build_path(target, params)
        )

        url = re.sub(r'/+', '/', url)
        return 'https://%s' % url

class UsergridSession(BaseSession):

    def __init__(self, org_name,
                 auth_level='application',
                 access_token=None,
                 client_id=None,
                 client_secret=None,
                 username=None,
                 password=None,
                 is_secure=True,
                 **kwargs):
        """Initialize a Usergrid session.

        :param auth_level: (optional) authentication level for the session. Must either be 'user', 'application', 'organization' or 'admin'. Default to 'application'.
        :param access_token: access_token, if you already have one.
        :param client_id: (optional) client_id is needed for 'application' and 'organization' authentication.
        :param client_secret: (optional) client_secret is needed for 'application' and 'organization' authentication.
        :param username: (optional) username is needed for 'user' authentication.
        :param password: (optional) password is needed for 'user' authentication.
        :param is_secure: If your usergrid app is not secure and doesn't need any token, set this to ``False``.
        """

        super(UsergridSession, self).__init__(org_name, **kwargs)

        if access_token and not isinstance(access_token, basestring):
            raise ValueError("'access_token' must be a string")

        assert auth_level in ['user', 'application', 'organization', 'admin'], \
            "expected auth_level of 'user', 'application', 'organization' or 'admin'"
        self.token = access_token
        self.auth_level = auth_level
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.is_secure = is_secure

    def set_token(self, access_token):
        """Attach an access token to the UsergridSession.
        """

        self.token = access_token

    def read_token(self, response):
        """Read the access token from a ``usergrid.rest.RESTResponse`` and configure the session.
        """

        assert 'access_token' in response.data, "Cannot read the access token"

        self.set_token(response.data['access_token'])

    def build_access_headers(self):
        """Build access headers for a future request.
        Returns a tuple of (headers, params). (Only params are used for now)
        """

        if not self.is_linked():
            self.authenticate()

        params = {'access_token': self.token}

        return {}, params

    def authenticate(self):
        """Authenticate the session based on the auth_level defined.
        """

        if self.is_linked(): return # already authenticated

        try:
            if self.auth_level == "user":
                if not self.username or not self.password:
                    raise ValueError("auth_level 'user' requires a username and password.")
                res = self.login_()
        except RESTError, e:
            raise UsergridException("Unable to authenticate: " + e.description)

        self.read_token(res)

    def login_(self):
        """Link the session using Legacy Auth"""

        data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }

        url = self.build_url('/token')
        return rest.post(url, data=data)
