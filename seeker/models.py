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

    def __str__(self):
        return f"{self.user.username}'s profile"
    
class Link(models.Model):
    profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name="links")
    url = models.URLField()

    def __str__(self):
        return self.url