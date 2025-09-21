from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    is_recruiter = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=True)

    active_role = models.CharField(
        max_length=10,
        choices=[("recruiter", "Recruiter"), ("seeker", "Seeker")],
        default="seeker"
    )
# Create your models here.
