from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from job.models import Job

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
        
        # Sample jobs with coordinates (Atlanta area)
        sample_jobs = [
            {
                'title': 'Senior Python Developer',
                'description': 'We are looking for an experienced Python developer to join our team. You will work on building scalable web applications and APIs.',
                'location': 'Atlanta, GA',
                'latitude': 33.7490,
                'longitude': -84.3880,
                'salary_min': 80000,
                'salary_max': 120000,
                'skills': 'Python, Django, PostgreSQL, AWS',
                'remote': False,
                'visa_sponsorship': True
            },
            {
                'title': 'Frontend React Developer',
                'description': 'Join our frontend team to build beautiful and responsive user interfaces using React and modern web technologies.',
                'location': 'Atlanta, GA',
                'latitude': 33.7600,
                'longitude': -84.3900,
                'salary_min': 70000,
                'salary_max': 100000,
                'skills': 'React, JavaScript, CSS, HTML',
                'remote': True,
                'visa_sponsorship': False
            },
            {
                'title': 'Data Scientist',
                'description': 'We need a data scientist to analyze large datasets and build machine learning models to drive business insights.',
                'location': 'Atlanta, GA',
                'latitude': 33.7400,
                'longitude': -84.3800,
                'salary_min': 90000,
                'salary_max': 130000,
                'skills': 'Python, Machine Learning, TensorFlow, SQL',
                'remote': False,
                'visa_sponsorship': True
            },
            {
                'title': 'DevOps Engineer',
                'description': 'Looking for a DevOps engineer to manage our cloud infrastructure and deployment pipelines.',
                'location': 'Atlanta, GA',
                'latitude': 33.7700,
                'longitude': -84.4000,
                'salary_min': 85000,
                'salary_max': 115000,
                'skills': 'Docker, Kubernetes, AWS, CI/CD',
                'remote': True,
                'visa_sponsorship': True
            },
            {
                'title': 'Full Stack Developer',
                'description': 'Seeking a full-stack developer to work on both frontend and backend components of our web application.',
                'location': 'Atlanta, GA',
                'latitude': 33.7300,
                'longitude': -84.3700,
                'salary_min': 75000,
                'salary_max': 110000,
                'skills': 'Python, JavaScript, React, Django',
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
            self.style.SUCCESS(f'Successfully created {created_count} sample jobs')
        )
