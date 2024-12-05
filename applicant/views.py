import time
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ApplicantProfileForm
from .models import Applicant, Job
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth import logout
from django.shortcuts import redirect
from tqdm import tqdm  # Import tqdm for loading spinner
from django.shortcuts import render
from .models import Applicant,  JobRecommendation
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .forms import FeedbackForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback
import json
from .models import JobRecommendation
from django.http import HttpResponse
from django.contrib import messages  # Add this import
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Job, Applicant, JobApplication



def is_admin(user):
    return user.is_superuser  # Check if the user has admin privileges

# Apply the decorator
@user_passes_test(is_admin)
def my_view(request):
    # Your view logic here
    return render(request, 'index.html')


@login_required
def profile(request):
    try:
        applicant = Applicant.objects.get(user=request.user)
    except Applicant.DoesNotExist:
        applicant = None

    job_recommendations = []
    similarity_scores = []
    recommendation_precision = 0.0
    total_similarity = 0.0  # Initialize total similarity score
    progress = 0  # Initialize progress bar value

    if applicant:
        # Combine applicant skills and experience to create a profile text
        applicant_text = f"{applicant.skills} {applicant.experience}".strip()

        if not applicant_text:
            return render(request, 'applicant/profile.html', {
                'form': ApplicantProfileForm(instance=applicant),
                'error': 'Please fill in your skills and experience to get job recommendations.'
            })

        # Fetch all jobs in the database
        jobs = Job.objects.all()

        if not jobs:
            return render(request, 'applicant/profile.html', {
                'form': ApplicantProfileForm(instance=applicant),
                'error': 'No jobs available to recommend.'
            })

        # Combine job data: Job Role, Company, Location, Job Experience, Skills/Description
        job_descriptions = [
            f"{job.job_role} {job.company} {job.location} {job.job_experience} {job.skills_description}"
            for job in jobs
        ]

        # Include the applicant's text for similarity calculation
        texts = [applicant_text] + job_descriptions

        # Create a TF-IDF Vectorizer to convert text to vectors
        vectorizer = TfidfVectorizer(stop_words='english')

        tfidf_matrix = vectorizer.fit_transform(texts)  # Transform the texts to TF-IDF vectors

        # Calculate the cosine similarity between the applicant's profile and job descriptions
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

        # Sort jobs by similarity score and get top 6 recommendations
        sorted_jobs = sorted(zip(cosine_similarities[0], jobs), reverse=True, key=lambda x: x[0])

        # Remove duplicates by checking job IDs
        unique_jobs = []
        seen_jobs = set()

        for _, job in sorted_jobs:
            if job.id not in seen_jobs:
                unique_jobs.append(job)
                seen_jobs.add(job.id)
            if len(unique_jobs) == 6:  # Limit to 6 jobs
                break

        job_recommendations = unique_jobs
        similarity_scores = [score for score, _ in sorted_jobs[:6]]  # Top 6 similarity scores

        # Calculate total similarity score
        total_similarity = sum(similarity_scores)

        # Recommendation Precision calculation
        threshold = 0.4  # Increase threshold for more relevant recommendations
        relevant_count = sum(1 for score in similarity_scores if score >= threshold)

        # Calculate precision as the percentage of relevant recommendations out of the top 6
        recommendation_precision = relevant_count / len(similarity_scores) if similarity_scores else 0.0

        # Save recommendations to the database
        for idx, (job, similarity_score) in enumerate(zip(job_recommendations, similarity_scores)):
            # Check if the recommendation already exists for the applicant and job
            if not JobRecommendation.objects.filter(applicant=applicant, job=job).exists():
                job_rec = JobRecommendation(
                    applicant=applicant,
                    job=job,
                    similarity_score=similarity_score,
                    is_relevant=similarity_score >= threshold  # Mark as relevant if similarity score is above threshold
                )
                job_rec.save()

                # Update progress for each recommendation saved (in this case, 100% is reached after 6 jobs)
                progress = int(((idx + 1) / len(job_recommendations)) * 100)
                print(f"Job Recommendations for Applicant: {applicant.user.username}\n{'-'*60}")
                for idx, (job, score) in enumerate(zip(job_recommendations, similarity_scores), start=1):
                    print(f"{idx}. Job: {job.job_role} at {job.company} | Similarity Score: {score:.4f}")
                print(f"{'-'*60}\nTotal Similarity Score: {total_similarity:.4f}")
                print(f"Recommendation Precision: {recommendation_precision * 100:.2f}%\n")

                    
    if request.method == 'POST':
        form = ApplicantProfileForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.user = request.user
            applicant.save()

            # Recalculate job recommendations after saving the updated profile
            applicant_text = f"{applicant.skills} {applicant.experience}".strip()

            if applicant_text:
                jobs = Job.objects.all()
                job_descriptions = [
                    f"{job.job_role} {job.company} {job.location} {job.job_experience} {job.skills_description}"
                    for job in jobs
                ]
                texts = [applicant_text] + job_descriptions

                vectorizer = TfidfVectorizer(stop_words='english')

                tfidf_matrix = vectorizer.fit_transform(texts)
                cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
                sorted_jobs = sorted(zip(cosine_similarities[0], jobs), reverse=True, key=lambda x: x[0])

                unique_jobs = []
                seen_jobs = set()

                for _, job in sorted_jobs:
                    if job.id not in seen_jobs:
                        unique_jobs.append(job)
                        seen_jobs.add(job.id)
                    if len(unique_jobs) == 6:  # Limit to 6 jobs
                        break

                job_recommendations = unique_jobs

                # Save recommendations to the database after profile update
                for idx, (job, similarity_score) in enumerate(zip(job_recommendations, similarity_scores)):
                    if not JobRecommendation.objects.filter(applicant=applicant, job=job).exists():
                        job_rec = JobRecommendation(
                            applicant=applicant,
                            job=job,
                            similarity_score=similarity_score,
                            is_relevant=similarity_score >= threshold
                        )
                        job_rec.save()

                        # Update progress for each recommendation saved
                        progress = int(((idx + 1) / len(job_recommendations)) * 100)
                        # Display updated recommendations on terminal
                        print(f"Updated Job Recommendations for Applicant {applicant.user.username}:")
                        for job, score in zip(job_recommendations, similarity_scores):
                            print(f"Job: {job.job_role} at {job.company}, Similarity Score: {score}")

                        print(f"Total Similarity: {total_similarity}")
                        if recommendation_precision == 1.0:
                          print("Recommendation Precision: 1.0000")
                        else:
                          print(f"Recommendation Precision: {recommendation_precision * 100:.2f}%")



            return redirect('profile')  # Redirect to profile after saving
    else:
        form = ApplicantProfileForm(instance=applicant)

    return render(request, 'applicant/profile.html', {
        'form': form,
        'job_recommendations': job_recommendations,
        'similarity_scores': similarity_scores,
        'recommendation_precision': recommendation_precision,
        'total_similarity': total_similarity,  # Pass the total similarity to the template
        'applicant': applicant,
        'progress': progress  # Pass progress bar value to template
    })




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Create the Applicant instance with default status
            applicant = Applicant.objects.create(user=user, status='applicant')

            # Redirect to the profile page directly to update personal information
            return redirect('profile')  # Redirect directly to the profile page to complete the profile
    else:
        form = UserCreationForm()
    return render(request, 'applicant/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to profile after logging in
        else:
            return render(request, 'applicant/login.html', {'error': 'Invalid credentials'})
    return render(request, 'applicant/login.html')

@login_required
def edit_personal_info(request):
    user = request.user
    applicant, created = Applicant.objects.get_or_create(user=user)

    if request.method == 'POST':
        print("Request POST data:", request.POST)  # Debug: Check if form data is being received

        form = ApplicantProfileForm(request.POST, request.FILES, instance=applicant)
        
        if form.is_valid():
            form.save()  # Save the updated applicant data
            messages.success(request, "Your personal information has been updated successfully.")
            return redirect('profile')  # Redirect to profile page after successful update
        else:
            print("Form errors:", form.errors)  # Debug: Check form errors if not valid
            return render(request, 'applicant/profile.html', {
                'form': form,
                'error': 'Please correct the errors in the form.'
            })

    else:
        form = ApplicantProfileForm(instance=applicant)

    return render(request, 'applicant/profile.html', {'form': form})


@login_required  # Ensure the user is logged in
def submit_feedback(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Extract the data from the form
            rating = data.get('feedbackRating')
            comments = data.get('feedbackComments')
            suggestions = data.get('feedbackSuggestions')
            applicant_id = data.get('applicantId')

            # Retrieve the applicant using the logged-in user's applicant ID
            applicant = request.user.applicant  # Assuming the applicant model is linked to the user model

            # Save the feedback data
            feedback = Feedback(
                applicant=applicant,  # Associate the logged-in user with the feedback
                rating=rating,
                feedback_text=comments,
                suggestions=suggestions
            )
            feedback.save()

            # Send success response
            return JsonResponse({'message': 'Feedback submitted successfully!'})
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=400)

def job_match_history(request):
    job_recommendations = JobRecommendation.objects.filter(applicant=request.user.applicant)

    # Log or print recommendations to debug
    for recommendation in job_recommendations:
        print(f"{recommendation.job.job_role}: {recommendation.is_relevant}")

    # Calculate precision
    total_recommendations = job_recommendations.count()
    relevant_recommendations = job_recommendations.filter(is_relevant=True).count()
    
    if total_recommendations > 0:
        recommendation_precision = relevant_recommendations / total_recommendations
    else:
        recommendation_precision = 0
    
    return render(request, 'profile.html', {
        'job_recommendations': job_recommendations,
        'recommendation_precision': recommendation_precision
    })
    




def some_view(request):
    applicant = Applicant.objects.get(user=request.user)
    return render(request, 'template_name.html', {'applicant': applicant})

def home(request):
    return render(request, 'applicant/home.html')


def about(request):
    return render(request, 'applicant/about.html')


def category(request):
    return render(request, 'applicant/category.html')


def contact(request):
    return render(request, 'applicant/contact.html')


def job_detail(request):
    return render(request, 'applicant/job-detail.html')


def job_list(request):
    return render(request, 'applicant/job-list.html')


def testimonial(request):
    return render(request, 'applicant/testimonial.html')


def index(request):
    return render(request, 'applicant/index.html')

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')  # Redirect to the home page after logout


def view_applicant(request):
    applicant = Applicant.objects.get(user=request.user)

    if applicant.status == 'staff':
        # Show staff-specific data
        return render(request, 'staff_dashboard.html')
    elif applicant.status == 'admin':
        # Show admin-specific data
        return render(request, 'admin_dashboard.html')
    else:
        # Show applicant-specific data
        return render(request, 'applicant_dashboard.html')

def apply_now(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applicant = get_object_or_404(Applicant, user=request.user)

    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')

        if cover_letter:
            # Save the job application with the cover letter
            job_application = JobApplication.objects.create(
                applicant=applicant,
                job=job,
                cover_letter=cover_letter,
            )

            # Return a JSON response indicating success along with application data
            data = {
                'status': 'success',
                'message': 'Your application has been submitted successfully.',
                'applicant_name': job_application.applicant.name,
                'job_role': job_application.job.job_role,
                'status': job_application.status,
                'application_date': job_application.application_date.strftime('%b %d, %Y, %I:%M %p'),
                'application_id': job_application.id,  # Pass application_id in response
            }

            return JsonResponse(data)
        else:
            # If no cover letter is provided
            return JsonResponse({
                'status': 'error',
                'message': 'Cover letter is required.',
            })

    return render(request, 'applicant/apply_form.html', {
        'job': job,
        'applicant': applicant,
    })


def job_application_status(request, application_id):
    jobapplication = get_object_or_404(JobApplication, id=application_id)
    return render(request, 'applicant/job_application_status.html', {
        'jobapplication': jobapplication
    })


def update_application_time(request, application_id):
    if request.method == 'POST':
        job_application = get_object_or_404(JobApplication, id=application_id)
        
        # Update the application date to the current time
        job_application.application_date = now()
        job_application.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Application date updated successfully.',
            'application_date': job_application.application_date.strftime('%b %d, %Y, %I:%M %p')
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})