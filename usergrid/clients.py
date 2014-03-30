# -*- coding: utf-8 -*-

"""
usergrid.clients
~~~~~~~~~~~~~~~~

This module contains the usergrid clients.
"""

from .sessions import BaseSession, UsergridSession
from .rest import RESTClient

class BaseClient(object):

    def __init__(self, session, rest_client=None):
        """Construct a ``BaseClient`` instance.
        Returns :class:`BaseClient`` object.

        :param session: an instance of :class:`UsergridSession`
        :param rest_client: Optional :class:`usergrid.rest.RESTClient` object to for making requests.
        """

        if rest_client is None: rest_client = RESTClient

        if isinstance(session, BaseSession):
            self.session = session
        else:
            raise ValueError("'session' must be a UsergridSession")

        self.rest = rest_client

    def request(self, target, params=None, method='POST'):
        """Construct the url, headers and params for a request with all access information.
        Returns a tuble of (url, headers, params).
        """

        assert method in ['GET','POST', 'PUT'], "Only 'GET', 'POST', and 'PUT' are allowed."

        if params is None:
            params = {}

        headers, access_params = self.session.build_access_headers()
        params =  dict(params.items() + access_params.items())

        if method in ('GET', 'PUT'):
            url = self.session.build_url(target, params)
        else:
            url = self.session.build_url(target)

        return url, headers, params


class ApplicationClient(BaseClient):
    """This class lets you make API calls to manage a Usergrid application. You'll need to obtain an
    OAuth2 access token first. You can get an access token using :class:`UsergridSession`
    """

    def __init__(self, *args, **kwargs):
        super(ApplicationClient, self).__init__(*args, **kwargs)

    def test(self):

        url, headers, params = self.request('/users')

        return self.rest.get(url)
