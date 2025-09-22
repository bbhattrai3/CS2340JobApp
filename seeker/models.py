from django.db import models
from django.conf import settings

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    projects = models.TextField()
    work_experience = models.TextField()
    skills = models.TextField()
    links = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"