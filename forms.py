from django import forms
from django.forms import ModelForm
from djangovoice.models import Feedback

class WidgetForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('type', 'anonymous', 'private', 'title', 'description',)

class EditForm(ModelForm):
    class Meta:
        model = Feedback
