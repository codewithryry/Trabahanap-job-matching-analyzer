# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Applicant, Job, JobRecommendation, Feedback

# Admin for Feedback
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'date_submitted', 'feedback_text')
    search_fields = ('applicant__name', 'feedback_text')

# Admin for JobRecommendation (renamed JobMatch to avoid conflicts)
class JobRecommendationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'match_date')  # Removed 'status' from here


# Registering models with custom admins
admin.site.register(JobRecommendation, JobRecommendationAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Applicant)
admin.site.register(Job)
