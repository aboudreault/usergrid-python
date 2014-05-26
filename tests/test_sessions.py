# -*- coding: utf-8 -*-

"""Tests for usergrid.sessions"""

import unittest

import httpretty
from httpretty.core import HTTPrettyRequest, HTTPrettyRequestEmpty

from usergrid.sessions import BaseSession, UsergridSession
from usergrid.exceptions import UsergridException

from .mock import MockUsergridResponse

class BaseSessionTestCase(unittest.TestCase):

    def setUp(self):
        self.sess = BaseSession('org_test',
                                api_url='api.example.com',
                                app_name='sandbox')

    def test_default_values(self):
        sess = BaseSession('org_test')
        self.assertEquals(sess.api_url, 'api.usergrid.com')
        self.assertEquals(sess.app_name, 'sandbox')

    def test_new_instance_values(self):
        sess = BaseSession('org_test',
                           api_url='api.test.com',
                           app_name='my_app'
        )
        self.assertEquals(sess.api_url, 'api.test.com')
        self.assertEquals(sess.app_name, 'my_app')

    def test_basic_building(self):
        self.assertEqual(self.sess.org_name, 'org_test')
        self.assertEqual(self.sess.api_url, 'api.example.com')
        self.assertEqual(self.sess.app_name, 'sandbox')
        self.assertIsNone(self.sess.token)

    def test_not_linked(self):
        self.assertFalse(self.sess.is_linked())

    def test_unlink(self):
        self.sess.token = 'test_token'
        self.assertTrue(self.sess.is_linked())
        self.sess.unlink()
        self.assertFalse(self.sess.is_linked())

    def test_simple_path(self):
        path = self.sess.build_path('users')
        self.assertEqual(path, '/users')

    def test_path_with_params(self):
        params = {'t': 3, 'w': 'test'}
        path = self.sess.build_path('users', params)
        self.assertEqual(path, '/users?t=3&w=test')

    def test_simple_url(self):
        url = self.sess.build_url('users')
        self.assertEqual(url, 'https://api.example.com/org_test/sandbox/users')

    def test_url_with_params(self):
        params = {'t': 3, 'w': 'test'}
        url = self.sess.build_url('users', params)
        self.assertEqual(url, 'https://api.example.com/org_test/sandbox/users?t=3&w=test')


class UsergridSessionTestCase(unittest.TestCase):

    def setUp(self):
        self.sess = UsergridSession('org_test',
                                    api_url='api.usergrid.com',
                                    app_name='sandbox',
                                    auth_level='user',
                                    username='test',
                                    password='test'
                                )

    def test_default_values(self):
        sess = UsergridSession('org_test')
        self.assertEquals(sess.api_url, 'api.usergrid.com')
        self.assertEquals(sess.app_name, 'sandbox')
        self.assertEquals(sess.auth_level, 'client')
        self.assertIsNone(sess.token)
        self.assertIsNone(sess.client_id)
        self.assertIsNone(sess.client_secret)
        self.assertIsNone(sess.username)
        self.assertIsNone(sess.password)
        self.assertTrue(sess.is_secure)

    def test_new_instance_values(self):
        sess = UsergridSession('org_test',
                               api_url='api.test.com',
                               app_name='my_app',
                               auth_level='user',
                               token='my_secret_token',
                               client_id='YXq6gmWImAA-EeO8UWQODUP8wQ',
                               client_secret='YXq6gm2WE3W-EeOWImAADUP8wQ',
                               username='test',
                               password='test',
                               is_secure=False
                           )
        self.assertEquals(sess.api_url, 'api.test.com')
        self.assertEquals(sess.app_name, 'my_app')
        self.assertEquals(sess.auth_level, 'user')
        self.assertEquals(sess.token, 'my_secret_token')
        self.assertEquals(sess.client_id, 'YXq6gmWImAA-EeO8UWQODUP8wQ')
        self.assertEquals(sess.client_secret, 'YXq6gm2WE3W-EeOWImAADUP8wQ')
        self.assertEquals(sess.username, 'test')
        self.assertEquals(sess.password, 'test')
        self.assertFalse(sess.is_secure)

    def test_new_instance_invalid_token(self):
        with self.assertRaises(ValueError):
            sess = UsergridSession('org_test', token=42)

    def test_new_instance_valid_token(self):
        sess = UsergridSession('org_test', token='test_token')
        self.assertEquals(sess.token, 'test_token')
        self.assertTrue(sess.is_linked())

    def test_set_token(self):
        self.assertIsNone(self.sess.token)
        self.sess.set_token('new_token')
        self.assertEquals(self.sess.token, 'new_token')

    @httpretty.activate
    def test_user_authenticate(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api.usergrid.com/org_test/sandbox/token',
            body=MockUsergridResponse.VALID_USER_AUTHENTICATION,
        )
        self.assertFalse(self.sess.is_linked())
        self.sess.authenticate()
        self.assertIsInstance(httpretty.last_request(), HTTPrettyRequest)
        self.assertTrue(self.sess.is_linked())

    @httpretty.activate
    def test_invalid_user_authenticate(self):
        sess = UsergridSession('org_test',
                               auth_level='user',
                               username='test',
                               password='wrong_password'
                           )

        httpretty.register_uri(
            httpretty.POST,
            'https://api.usergrid.com/org_test/sandbox/token',
            body=MockUsergridResponse.INVALID_USER_AUTHENTICATION,
            status=400
        )
        with self.assertRaises(UsergridException):
            sess.authenticate()
        self.assertFalse(sess.is_linked())

    def test_missing_info_user_authenticate(self):
        sess = UsergridSession('org_test',
                               auth_level='user',
                               username='test'
                           )

        with self.assertRaises(ValueError):
            sess.authenticate()
        self.assertFalse(sess.is_linked())

    @httpretty.activate
    def test_already_authenticated(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api.usergrid.com/org_test/sandbox/token',
            body=MockUsergridResponse.VALID_USER_AUTHENTICATION,
        )
        self.assertFalse(self.sess.is_linked())
        self.sess.set_token('test_token')
        self.sess.authenticate()
        self.assertIsInstance(httpretty.last_request(), HTTPrettyRequestEmpty)
