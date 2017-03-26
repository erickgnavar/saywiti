from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView

from .forms import IssueForm
from .models import Issue, Project


class ProjectDetailView(DetailView):

    template_name = 'projects/project_detail.html'
    model = Project
    pk_url_karg = 'slug'
    context_object_name = 'project'


class IssueDetailView(DetailView):

    template_name = 'projects/issue_detail.html'
    model = Issue
    pk_url_kwarg = 'id'
    context_object_name = 'issue'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'related_issues': self._get_related_issues()
        })
        return context

    def _get_related_issues(self):
        return Issue.objects.filter(category=self.object.category).order_by('-created').exclude(id=self.object.id)[:10]


class IssueCreateView(CreateView):

    template_name = 'projects/issue_create.html'
    model = Issue
    form_class = IssueForm

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'project': self.project
        })
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse('projects:project-detail', kwargs={'slug': self.project.slug})
