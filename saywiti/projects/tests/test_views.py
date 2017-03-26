from django.contrib.gis.geos import Point
from django.core.urlresolvers import resolve
from django.http import Http404
from django.test import RequestFactory, TestCase

from mixer.backend.django import mixer

from .. import views
from ..models import Issue


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


class IssueCreateViewTestCase(TestCase):

    def setUp(self):
        self.view = views.IssueCreateView.as_view()
        self.factory = RequestFactory()
        self.project = mixer.blend('projects.Project')
        self.category = mixer.blend('projects.Category', project=self.project)

    def test_match_expected_view(self):
        url = resolve('/projects/{}/new-issue/'.format(self.project.slug))
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_render(self):
        response = self.client.get('/projects/{}/new-issue/'.format(self.project.slug))
        self.assertEqual(response.status_code, 200)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        response = self.view(request, slug=self.project.slug)
        self.assertEqual(response.status_code, 200)

    def test_create_issue(self):
        request = self.factory.post('/', {
            'title': 'test',
            'content': 'test',
            'category': self.category.id,
            'point': 'POINT (0 0)'
        })
        self.assertEqual(Issue.objects.filter(project=self.project).count(), 0)
        response = self.view(request, slug=self.project.slug)
        self.assertEqual(Issue.objects.filter(project=self.project).count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_error_with_missed_point(self):
        request = self.factory.post('/', {
            'title': 'test',
            'content': 'test',
            'category': self.category.id
        })
        self.assertEqual(Issue.objects.filter(project=self.project).count(), 0)
        response = self.view(request, slug=self.project.slug)
        self.assertEqual(Issue.objects.filter(project=self.project).count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertIn('point', response.context_data['form'].errors)

    def test_project_not_found(self):
        request = self.factory.get('/projects/not-found-projects/new-issue/')
        with self.assertRaises(Http404):
            self.view(request, id=9999)
