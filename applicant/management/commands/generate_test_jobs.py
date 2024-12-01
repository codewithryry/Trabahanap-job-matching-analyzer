from itertools import product
import random
from applicant.models import Job

# Define job titles, descriptions, and skills
job_titles = ["Software Engineer", "Data Scientist", "Product Manager", "UX/UI Designer", "Business Analyst"]
job_descriptions = [
    "Develop and maintain software applications.",
    "Analyze data to help businesses make informed decisions.",
    "Oversee the development of products from inception to launch.",
    "Design user interfaces and improve user experiences.",
    "Analyze business processes and recommend improvements."
]
job_skills = [
    "Python, Django, JavaScript, React",
    "Data Analysis, Machine Learning, Python, R",
    "Project Management, Scrum, Agile, Jira",
    "UI/UX Design, Figma, Prototyping, HTML/CSS",
    "Business Analysis, SQL, Tableau, Excel"
]

# Generate all possible unique combinations
all_combinations = list(product(job_titles, job_descriptions, job_skills))
random.shuffle(all_combinations)  # Shuffle to randomize the order

# Truncate or repeat combinations to reach 10 million
desired_jobs = 10_000_000
unique_jobs = all_combinations * (desired_jobs // len(all_combinations)) + all_combinations[:desired_jobs % len(all_combinations)]

# Insert jobs into the database
for title, description, skills in unique_jobs:
    Job.objects.create(title=title, description=description, required_skills=skills)

print("Successfully added 10 million unique jobs!")
