from django import forms

from experiment.models import ExperimentModel


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = ExperimentModel
        fields = ("name",)
