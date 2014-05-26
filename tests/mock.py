# -*- coding: utf-8 -*-

class MockUsergridResponse(object):
    """
    Usergrid Server Responses mocking.
    """

    INVALID_USER_AUTHENTICATION = """
    {
      "error": "invalid_grant",
      "error_description": "invalid username or password"
    }
    """

    VALID_USER_AUTHENTICATION = """
    {
      "access_token": "YWMta8JRhuN3EeOvQAtG5uTxBwAAAUZTswZHjuTGWM5Gj_tOvh21u8MzvXe0XLU",
      "expires_in": 604800,
      "user": {
        "activated": true,
        "created": 1395501601690,
        "email": "test@test.com",
        "modified": 1400958775098,
        "name": "test",
        "picture": "http://www.gravatar.com/avatar/9937c10c20deedb426ea5a6ee64745cd",
        "type": "user",
        "username": "test",
        "uuid": "7006efaa-b1d5-11e3-9854-5172c2613646"
       }
    }
"""
