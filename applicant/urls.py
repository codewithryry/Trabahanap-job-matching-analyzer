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
]
