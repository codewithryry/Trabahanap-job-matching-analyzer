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

@login_required
def profile(request):
    try:
        applicant = Applicant.objects.get(user=request.user)
    except Applicant.DoesNotExist:
        applicant = None

    job_recommendations = []
    similarity_scores = []
    recommendation_precision = 0.0

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

        # Start showing a loading spinner while TF-IDF is being calculated
        print("Calculating job recommendations...")

        # Show progress bar for calculating recommendations
        with tqdm(total=1, desc="Calculating TF-IDF and Cosine Similarities", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            tfidf_matrix = vectorizer.fit_transform(texts)  # Transform the texts to TF-IDF vectors
            pbar.update(1)  # Update progress bar after processing

        # Calculate the cosine similarity between the applicant's profile and job descriptions
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

        # Sort jobs by similarity score and get top 6 recommendations (instead of 10)
        sorted_jobs = sorted(zip(cosine_similarities[0], jobs), reverse=True, key=lambda x: x[0])

        # Remove duplicates by checking job IDs
        unique_jobs = []
        seen_jobs = set()

        for _, job in sorted_jobs:
            if job.id not in seen_jobs:
                unique_jobs.append(job)
                seen_jobs.add(job.id)
            if len(unique_jobs) == 6:  # Change to 6 jobs
                break

        job_recommendations = unique_jobs
        similarity_scores = [score for score, _ in sorted_jobs[:6]]  # Top 6 similarity scores

        # Log similarity scores distribution
        print("\nSimilarity Scores Distribution:")
        print(similarity_scores)

        # Recommendation Precision calculation
        threshold = 0.4  # Increase threshold for more relevant recommendations
        relevant_count = sum(1 for score in similarity_scores if score >= threshold)

        # Calculate precision as the percentage of relevant recommendations out of the top 6
        recommendation_precision = relevant_count / len(similarity_scores) if similarity_scores else 0.0

        # Print top recommendations with similarity scores and precision to the terminal
        print("\nTop Recommendations:")
        for idx, job in enumerate(job_recommendations, start=1):
            print(f"{idx}. {job.job_role} | Similarity: {similarity_scores[idx-1]:.4f}")

        print(f"\nRecommendation Precision: {recommendation_precision:.4f}")

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

                # Use tqdm to show a loading spinner while TF-IDF is being calculated
                print("Recalculating job recommendations after profile update...")
                with tqdm(total=1, desc="Calculating TF-IDF and Cosine Similarities", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                    tfidf_matrix = vectorizer.fit_transform(texts)
                    pbar.update(1)

                cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
                sorted_jobs = sorted(zip(cosine_similarities[0], jobs), reverse=True, key=lambda x: x[0])

                unique_jobs = []
                seen_jobs = set()

                for _, job in sorted_jobs:
                    if job.id not in seen_jobs:
                        unique_jobs.append(job)
                        seen_jobs.add(job.id)
                    if len(unique_jobs) == 6:  # Change to 6 jobs
                        break

                job_recommendations = unique_jobs

            return redirect('profile')  # Redirect to profile after saving
    else:
        form = ApplicantProfileForm(instance=applicant)

    return render(request, 'applicant/profile.html', {
        'form': form,
        'job_recommendations': job_recommendations,
        'similarity_scores': similarity_scores,
        'recommendation_precision': recommendation_precision,
        'applicant': applicant  # Pass the applicant object to the template
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
        # Update the applicant's personal information
        applicant.name = request.POST.get('name')
        applicant.email = request.POST.get('email')
        applicant.skills = request.POST.get('skills')
        applicant.experience = request.POST.get('experience')
        
        # Update the resume if provided
        if 'resume' in request.FILES:
            applicant.resume = request.FILES['resume']
        
        # Save the updated applicant information
        applicant.save()

        # Recalculate job recommendations based on the new skills
        job_recommendations = calculate_job_recommendations(applicant.skills)
        
        # Redirect to the profile page with updated job recommendations
        return redirect('profile')  # Pass job_recommendations if needed
        
    # Get the current job recommendations
    job_recommendations = calculate_job_recommendations(applicant.skills)
    
    # Render the template with the updated applicant information and job recommendations
    return render(request, 'template_name.html', {
        'applicant': applicant,
        'job_recommendations': job_recommendations,
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