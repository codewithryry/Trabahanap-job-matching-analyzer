# applicant/forms.py
from django import forms
from .models import Applicant

class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'skills', 'experience', 'resume']

