from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    active_role = models.CharField(
        max_length=10,
        choices=[("recruiter", "Recruiter"), ("seeker", "Seeker")],
        default='seeker'
    )
# Create your models here.
