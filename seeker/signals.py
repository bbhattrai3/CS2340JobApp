from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import JobSeekerProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_jobseeker_profile(sender, instance, created, **kwargs):
    if created and instance.role == "seeker":
        JobSeekerProfile.objects.create(user=instance)