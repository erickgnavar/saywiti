from django import forms

from .models import Issue


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ('title', 'category', 'content', 'point')
        widgets = {
            'point': forms.HiddenInput
        }

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        self.fields['category'].queryset = self.project.categories.all()

    def save(self, commit=True):
        issue = super().save(commit=False)
        issue.project = self.project
        issue.save()
        return issue
