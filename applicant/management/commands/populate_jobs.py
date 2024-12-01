import csv
from django.core.management.base import BaseCommand
from applicant.models import Job

class Command(BaseCommand):
    help = 'Populate job data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                Job.objects.create(
                    job_role=row['Job_Role'],
                    company=row['Company'],
                    location=row['Location'],
                    job_experience=row['Job Experience'],
                    skills_description=row['Skills/Description']
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated job data from {csv_file}!'))
