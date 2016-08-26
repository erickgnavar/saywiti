# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve

from .. import views


class HomeViewTestCase(TestCase):

    def setUp(self):
        self.view = views.home
        self.factory = RequestFactory()

    def test_match_expected_view(self):
        url = resolve('/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
