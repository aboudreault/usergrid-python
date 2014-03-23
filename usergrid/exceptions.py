# -*- coding: utf-8 -*-

"""
usergrid.exceptions
~~~~~~~~~~~~~

This module contains the set of Usergrid' exceptions.
"""

import datetime

class UsergridException(IOError):
    """Represents a Usergrid Exception"""

    def __init__(self, *args, **kwargs):
        """Constructs the Usergrid Exception.

        :param exception: (optional) The original exception. (ie. A ``requests.exceptions.ConnectionError``)
        """

        super(UsergridException, self).__init__(*args, **kwargs)


class RESTError(UsergridException):
    """A class that represents a usergrid error.
    """

    def __init__(self, data, *args, **kwargs):
        """Constructs the REST Error.

        :param data: A dictionary of the response data.
        """
        self.error = data['error']
        self.description = data['error_description']

        self.timestamp = data['timestamp'] if 'timestamp' in data else datetime.datetime.now()
        self.exception_name = data['exception'] if 'exception' in data else None
        super(RESTError, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<RESTError ["%s": %s]' % (self.error, self.description)

    def __str__(self):
        return self.__repr__()
