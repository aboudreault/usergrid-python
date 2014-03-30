# -*- coding: utf-8 -*-

"""
usergrid.rest
~~~~~~~~~~~~~

This module contains the usergrid rest abstraction objects. It is used
internally by ``usergrid.client`` and ``usergrid.session``.
"""

import requests
from requests.exceptions import RequestException

from .exceptions import (
    UsergridException,
    RESTError
)


class RESTResponse(object):
    """A class that represents a Usergrid REST json response.
    """

    def __init__(self, response):
        """Constructs a REST Response.

        :param response: The ``requests.Response`` object.
        """

        self.headers = response.headers
        self.status = response.status_code
        self.data = response.json()
        self.encoding = response.encoding
        self.data = response.json()


class RESTClientImpl(object):
    """This is the RESTClient implementation.

    Currently this class is not really useful since we are simply using requests directly without
    premature optimization. But it will be useful later with the use of ``requests.Session`` and/or
    ``requests.Request`` for various configuration and optimization (ie connection-pooling).

    """

    def __init__(self):
        """Initialize a RESTClientImpl instance.
        """
        pass

    def request(self, method, url, **kwargs):
        """Make a REST request.

        :param method: The http method of the request.
        :param url:  The url of the request.
        :param \*\*kwargs: Optional arguments that ``requests.request`` takes.
        """

        try:
            res = requests.request(method, url, **kwargs)
        except RequestException, e:
            raise UsergridException(str(e))

        if res.status_code != 200:
            raise RESTError(res.json())

        return RESTResponse(res)


class RESTClient(object):
    """A class with all static methods to perform JSON REST requests. Used internally by the Usergrid
    Client.
    """

    IMPL = RESTClientImpl()

    @classmethod
    def get(cls, url, **kwargs):
        """Make a GET request.

        :param url: The url of the request.
        :param \*\*kwargs: Optional arguments that ``requests.request`` takes.
        """

        return cls.IMPL.request('GET', url, **kwargs)

    @classmethod
    def post(cls, url, data=None, **kwargs):
        """Make a POST request.

        :param url: The url of the request.
        :param data: (optional) A dictionary of the post parameters. Default to None.
        :param \*\*kwargs: Optional arguments that ``requests.request`` takes.
        """
        return cls.IMPL.request('POST', url, data=data, **kwargs)
