from django.contrib.auth.models import User
from django.db import models

class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Use only OneToOneField
    name = models.CharField(max_length=100)
    email = models.EmailField()
    skills = models.TextField()
    experience = models.TextField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    job_role = models.CharField(max_length=255, default="Unknown Role")
    company = models.CharField(max_length=255, default="Unknown")
    location = models.CharField(max_length=255, default="Not specified")
    job_experience = models.CharField(max_length=255, default="Not specified")
    skills_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_role
