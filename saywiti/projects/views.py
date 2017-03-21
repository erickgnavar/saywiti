from django.views.generic import DetailView

from .models import Project, Issue


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
