from django.http import Http404
from django.test import RequestFactory, TestCase

from django.contrib.gis.geos import Point
from django.core.urlresolvers import resolve

from .. import views
from mixer.backend.django import mixer


class ProjectDetailViewTestCase(TestCase):

    def setUp(self):
        self.view = views.ProjectDetailView.as_view()
        self.factory = RequestFactory()
        self.project = mixer.blend('projects.Project')

    def test_match_expected_view(self):
        url = resolve('/projects/{}/'.format(self.project.slug))
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_render(self):
        response = self.client.get('/projects/{}/'.format(self.project.slug))
        self.assertEqual(response.status_code, 200)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        response = self.view(request, slug=self.project.slug)
        self.assertEqual(response.status_code, 200)
        self.assertIn('project', response.context_data)

    def test_not_found(self):
        request = self.factory.get('/')
        with self.assertRaises(Http404):
            self.view(request, slug='error')


class IssueDetailViewTestCase(TestCase):

    def setUp(self):
        self.view = views.IssueDetailView.as_view()
        self.factory = RequestFactory()
        self.issue = mixer.blend('projects.Issue', point=Point((-80.6201499999999953, -5.2004500000000000)))

    def test_match_expected_view(self):
        url = resolve('/issues/{}/'.format(self.issue.id))
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_render(self):
        response = self.client.get('/issues/{}/'.format(self.issue.id))
        self.assertEqual(response.status_code, 200)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        response = self.view(request, id=self.issue.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('issue', response.context_data)
        self.assertIn('related_issues', response.context_data)

    def test_not_found(self):
        request = self.factory.get('/')
        with self.assertRaises(Http404):
            self.view(request, id=9999)
