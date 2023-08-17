from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    recaptcha = forms.CharField()

    class Meta:
        model = Feedback
        fields = ['email', 'name', 'message', 'phone']