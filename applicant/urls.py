from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import CustomLogoutView






urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('category/', views.category, name='category'),  # Job categories
    path('contact/', views.contact, name='contact'),  # Contact form
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.login_view, name='login'),  # User login
    path('profile/', views.profile, name='profile'),  # User profile
    path('job-detail/', views.job_detail, name='job-detail'),  # Job details
    path('job-list/', views.job_list, name='job-list'),  # Job list
    path('testimonials/', views.testimonial, name='testimonial'),  # Testimonials
    path('index/', views.index,  name='index'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('apply/<int:job_id>/', views.apply_now, name='apply_now'),
    path('edit-personal-info/', views.edit_personal_info, name='edit_personal_info'),
    path('application-status/<int:application_id>/', views.job_application_status, name='job_application_status'),
    path('update-application-time/', views.update_application_time, name='update_application_time'),
]
