from django.core.management.base import BaseCommand
from applicant.models import Job

class Command(BaseCommand):
    help = 'Removes duplicate job entries from the database'

    def handle(self, *args, **kwargs):
        # Fetch all job instances
        jobs = Job.objects.all()

        print(f"Total jobs to check: {jobs.count()}")  # Debugging: print the number of jobs

        # Dictionary to track seen job combinations (description, required_skills)
        seen_jobs = {}

        for job in jobs:
            job_key = (job.description, job.required_skills)  # Unique key to check duplicates

            if job_key not in seen_jobs:
                seen_jobs[job_key] = job
            else:
                # Delete the duplicate job (keeping the first one)
                print(f"Deleting duplicate job: {job.title} - {job.description}")  # Debugging: which job is deleted
                job.delete()

        self.stdout.write(self.style.SUCCESS('Successfully removed duplicate job entries'))
