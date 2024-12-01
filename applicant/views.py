from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View  # Import the View class
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ApplicantProfileForm
from .models import Applicant, Job
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth import logout
from django.shortcuts import redirect





@login_required
def profile(request):
    try:
        applicant = Applicant.objects.get(user=request.user)
    except Applicant.DoesNotExist:
        applicant = None

    job_recommendations = []

    if applicant:
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

        # Combine applicant text and job descriptions into a list
        job_descriptions = [job.description + " " + job.required_skills for job in jobs]

        # Include the applicant's text for similarity calculation
        texts = [applicant_text] + job_descriptions

        # Create a TF-IDF Vectorizer to convert text to vectors
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Calculate the cosine similarity between the applicant's profile and job descriptions
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

        # Sort jobs by similarity score and get top 5 recommendations
        sorted_jobs = sorted(zip(cosine_similarities[0], jobs), reverse=True, key=lambda x: x[0])
        job_recommendations = [job for _, job in sorted_jobs[:5]]

    if request.method == 'POST':
        form = ApplicantProfileForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.user = request.user  # Ensure the applicant is linked to the current user
            applicant.save()
            return redirect('profile')  # Redirect to profile after saving
    else:
        form = ApplicantProfileForm(instance=applicant)

    return render(request, 'applicant/profile.html', {
        'form': form,
        'job_recommendations': job_recommendations
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to profile after registering
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


def edit_personal_info(request):
    applicant, created = Applicant.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        applicant.name = request.POST.get('name')
        applicant.email = request.POST.get('email')
        applicant.skills = request.POST.get('skills')
        applicant.experience = request.POST.get('experience')
        
        if 'resume' in request.FILES:
            applicant.resume = request.FILES['resume']
        
        applicant.save()
        return redirect('profile')  # Adjust redirection as needed
    
    return render(request, 'template_name.html', {'applicant': applicant})


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