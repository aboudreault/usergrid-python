# -*- coding: utf-8 -*-

class MockUsergridResponse(object):
    """
    Usergrid Server Responses mocking.
    """

    INVALID_AUTHENTICATION = """
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

    VALID_CLIENT_AUTHENTICATION = r"""
    {
      "access_token": "YWMtrgpwmuU6EeOCJYd-biDFPgAAAUZfQGUb42JUujfPnB1NSp9-rsX0nuWI_Vk",
      "expires_in": 604800,
      "organization": {
        "applications": {
            "org_test/sandbox": "4d1e186b-b001-11e2-9658-02e81af864a4",
            "org_test/test": "17651640-003e-11e3-aaea-09962263fcc1"
        },
        "name": "test",
        "passwordHistorySize": 0,
        "properties": {},
        "users": {
            "test": {
                "activated": true,
                "adminUser": true,
                "applicationId": "00000000-0000-0000-0000-000000000001",
                "confirmed": true,
                "disabled": false,
                "displayEmailAddress": "Test User <test@test.com>",
                "email": "test@test.com",
                "htmldisplayEmailAddress": "Test &lt;<a href=\"mailto:test@test.com\">test@test.com</a>&gt;",
                "name": "Test User",
                "properties": {
                    "passwordPolicyId": "15"
                },
                "username": "test",
                "uuid": "4c24769f-b001-11e2-9658-02e81af864a4"
            }
         },
        "uuid": "4c80eebc-b001-11e2-9658-02e81af864a4"
      }
    }
    """
