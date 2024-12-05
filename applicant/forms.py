# applicant/forms.py
from django import forms
from .models import Applicant
from .models import Feedback

class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'skills', 'experience']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['applicant', 'feedback_text', 'rating', 'suggestions']

