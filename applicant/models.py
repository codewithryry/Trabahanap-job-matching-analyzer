from django.contrib.auth.models import User
from django.db import models


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='applicant')  # Ensure this field exists 
    name = models.CharField(max_length=100)
    email = models.EmailField()
    skills = models.TextField()
    experience = models.TextField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Removed Status Field
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


# models.py
class Feedback(models.Model):
    applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], null=True, blank=True)
    suggestions = models.TextField(null=True, blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.applicant.name} on {self.date_submitted}'


class JobRecommendation(models.Model):
    applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    match_date = models.DateTimeField(auto_now_add=True)
    similarity_score = models.FloatField()
    is_relevant = models.BooleanField(default=False)  # Default is False

    def __str__(self):
        return f'{self.applicant.name} - {self.job.job_role}'


# class JobApplication(models.Model):
#     applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE)
#     job = models.ForeignKey('Job', on_delete=models.CASCADE)
#     cover_letter = models.TextField()
#     application_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Application from {self.applicant.name} for {self.job.job_role}'



class JobApplication(models.Model):
    applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    cover_letter = models.TextField()
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Pending')  # Default status

    def __str__(self):
        return f'Application from {self.applicant.name} for {self.job.job_role}'
