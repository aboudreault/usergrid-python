# -*- coding: utf-8 -*-

"""Tests for Usergrid."""

import unittest

from usergrid.sessions import BaseSession

class BaseSessionTestCase(unittest.TestCase):

    def setUp(self):
        self.sess = BaseSession('ORG_TEST',
                                api_url='api.example.com',
                                app_name='sandbox')

    def test_basic_building(self):
        self.assertEqual(self.sess.org_name, 'ORG_TEST')
        self.assertEqual(self.sess.api_url, 'api.example.com')
        self.assertEqual(self.sess.app_name, 'sandbox')
        self.assertIsNone(self.sess.token)

    def test_not_linked(self):
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
        self.assertEqual(url, 'https://api.example.com/ORG_TEST/sandbox/users')

    def test_url_with_params(self):
        params = {'t': 3, 'w': 'test'}
        url = self.sess.build_url('users', params)
        self.assertEqual(url, 'https://api.example.com/ORG_TEST/sandbox/users?t=3&w=test')
