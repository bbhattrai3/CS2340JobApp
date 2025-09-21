from django.db import models
from django.conf import settings

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255, default="")
    education = models.CharField(max_length=255, default="")
    work_experience = models.TextField(default="")
    skills = models.TextField(default="")
    links = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"