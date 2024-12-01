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
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.TextField()  # Skills required for the job
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

        