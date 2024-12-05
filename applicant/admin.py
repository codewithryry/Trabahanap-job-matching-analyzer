from django.contrib import admin
from django.utils.html import format_html
from .models import Applicant, Job, JobRecommendation, Feedback, JobApplication  # Import JobApplication


# Admin for Feedback
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'date_submitted', 'feedback_text')
    search_fields = ('applicant__name', 'feedback_text')

# Admin for JobRecommendation (renamed JobMatch to avoid conflicts)
class JobRecommendationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'match_date')  # Removed 'status' from here

# Admin for JobApplication
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'application_date')  # Display status and application date
    list_filter = ('status',)  # Add filter options for status
    search_fields = ('applicant__user__first_name', 'applicant__user__last_name', 'job__job_role')  # Search by applicant and job role

# Registering models with custom admins
admin.site.register(JobRecommendation, JobRecommendationAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Applicant)
admin.site.register(Job)
admin.site.register(JobApplication, JobApplicationAdmin)  # Register JobApplication with its custom admin
