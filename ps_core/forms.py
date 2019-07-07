from django import forms
from django.forms import models

from ps_core.models import UpdateRequest


class UpdateRequestCreateForm(models.ModelForm):

    class Meta:
        model = UpdateRequest
        fields = ('rank_req', 'reason',)
        widgets = {
            'reason': forms.Textarea(attrs={'style':'width: 100%; height: 5em;'})
        }


class UpdateRequestApproveForm(models.ModelForm):

    class Meta:
        model = UpdateRequest
        fields = ('status', 'comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'style':'width: 100%; height: 5em;'})
        }