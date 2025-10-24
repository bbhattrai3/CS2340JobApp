from django.core.management.base import BaseCommand
from job.models import Job
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Add sample jobs with coordinates for testing the map feature'

    def handle(self, *args, **options):
        # Get or create a recruiter user
        recruiter, created = User.objects.get_or_create(
            username='recruiter1',
            defaults={
                'email': 'recruiter1@example.com',
                'first_name': 'John',
                'last_name': 'Recruiter',
                'role': 'recruiter'
            }
        )
        
        # Sample job data with coordinates (Atlanta area)
        sample_jobs = [
            {
                'title': 'Senior Python Developer',
                'description': 'We are looking for an experienced Python developer to join our team. Must have experience with Django, Flask, and REST APIs.',
                'location': 'Atlanta, GA',
                'latitude': 33.7490,
                'longitude': -84.3880,
                'salary_min': 80000,
                'salary_max': 120000,
                'skills': 'Python, Django, REST API, PostgreSQL',
                'remote': False,
                'visa_sponsorship': True
            },
            {
                'title': 'Frontend React Developer',
                'description': 'Join our frontend team to build amazing user experiences. Experience with React, TypeScript, and modern CSS required.',
                'location': 'Atlanta, GA',
                'latitude': 33.7550,
                'longitude': -84.3900,
                'salary_min': 70000,
                'salary_max': 100000,
                'skills': 'React, TypeScript, CSS, HTML',
                'remote': True,
                'visa_sponsorship': False
            },
            {
                'title': 'Data Scientist',
                'description': 'Looking for a data scientist to work on machine learning projects. Experience with Python, pandas, scikit-learn required.',
                'location': 'Atlanta, GA',
                'latitude': 33.7600,
                'longitude': -84.3850,
                'salary_min': 90000,
                'salary_max': 130000,
                'skills': 'Python, Machine Learning, Pandas, Scikit-learn',
                'remote': False,
                'visa_sponsorship': True
            },
            {
                'title': 'DevOps Engineer',
                'description': 'We need a DevOps engineer to manage our cloud infrastructure. Experience with AWS, Docker, and Kubernetes required.',
                'location': 'Atlanta, GA',
                'latitude': 33.7450,
                'longitude': -84.3950,
                'salary_min': 85000,
                'salary_max': 125000,
                'skills': 'AWS, Docker, Kubernetes, Terraform',
                'remote': True,
                'visa_sponsorship': True
            },
            {
                'title': 'Full Stack Developer',
                'description': 'Join our full-stack development team. Experience with both frontend and backend technologies required.',
                'location': 'Atlanta, GA',
                'latitude': 33.7650,
                'longitude': -84.3800,
                'salary_min': 75000,
                'salary_max': 110000,
                'skills': 'JavaScript, Node.js, React, MongoDB',
                'remote': False,
                'visa_sponsorship': False
            }
        ]
        
        created_count = 0
        for job_data in sample_jobs:
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                recruiter=recruiter,
                defaults=job_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created job: {job.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample jobs with coordinates')
        )