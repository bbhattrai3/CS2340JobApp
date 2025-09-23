from django.db import models
from django.conf import settings

class Job(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    remote = models.BooleanField(default=False)
    salary_min = models.PositiveIntegerField(blank=True, null=True)
    salary_max = models.PositiveIntegerField(blank=True, null=True)
    visa_sponsorship = models.BooleanField(default=False)
    skills = models.CharField(max_length=300, blank=True, help_text="Comma-separated skills")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
