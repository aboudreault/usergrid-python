# -*- coding: utf-8 -*-

"""
usergrid.client
~~~~~~~~~~~~~~~

This module contains the usergrid client.
"""

from .session import BaseSession, UsergridSession

class UsergridClient(object):
    """
    This class lets you make Usergrid API calls. You'll need to obtain an OAuth2 access token first. You can get an access token using :class:`UsergridSession`
    """
    def __init__(self, access_token, rest_client=None):
        """Construct a ``UsergridClient`` instance.
        Returns :class:`UsergridClient`` object.

        :param access_token: an access_token (string) or an instance of a :class:`BaseSession`
        :param rest_client: Optional :class:`usergrid.rest.RESTClient` object to for making requests.
        """

        if rest_client is None: rest_client = RESTClient

        if isinstance(access_token, basestring):
            self.session = UsergridSession(access_token)
        elif isinstance(access_token, BaseSession):
            self.session = access_token
        else:
            raise ValueError("'access_token' must either be a string or a UsergridSession")

        self.rest_client = rest_client
