import csv
from django.core.management.base import BaseCommand
from applicant.models import Job  # Adjust to your model path

class Command(BaseCommand):
    help = 'Import job data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    Job.objects.create(
                        title=row['Job_Role'],  # Map columns from the CSV to the model fields
                        company=row['Company'],
                        location=row['Location'],
                        job_experience=row['Job Experience'],
                        skills_description=row['Skills/Description']
                    )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {csv_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
