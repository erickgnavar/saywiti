import json

from django.contrib.gis.geos import Point
from django.core.urlresolvers import resolve
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer

from .. import views


class IssueListViewTestCase(TestCase):

    def setUp(self):
        self.view = views.issue_list
        self.factory = RequestFactory()
        self.project = mixer.blend('projects.Project')
        self.category = mixer.blend('projects.Category')
        fields = {
            'project': self.project,
            'category': self.category,
            'point': Point((-80.6201499999999953, -5.2004500000000000))
        }
        self.issues = mixer.cycle(2).blend('projects.Issue', **fields)

    def test_match_expected_view(self):
        url = resolve('/api/v1/projects/{}/issues/'.format(self.project.slug))
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        response = self.view(request, slug=self.project.slug)
        body = json.loads(response.content.decode('utf8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', body)
        self.assertEqual(len(body['data']), 2)
