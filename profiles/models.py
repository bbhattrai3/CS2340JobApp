"""
from django.db import models
from django.contrib.auth.models import User

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Inherit from User
    headline = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    work_experience = models.TextField()
    skills = models.TextField()
    links = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

"""