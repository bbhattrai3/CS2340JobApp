import csv
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import get_user_model

from job.models import Job
from seeker.models import JobSeekerProfile, Link

User = get_user_model()


def export_all_data(request):
    """Global export for all admin data (CSV)."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="JobApp_Export.csv"'
    writer = csv.writer(response)

    # ============ SUMMARY ============
    writer.writerow(["===== Platform Summary ====="])
    writer.writerow(["Total Users", User.objects.count()])
    writer.writerow(["Total Job Seekers", JobSeekerProfile.objects.count()])
    writer.writerow(["Total Recruiters (with Jobs)", User.objects.filter(job__isnull=False).distinct().count()])
    writer.writerow(["Total Jobs", Job.objects.count()])
    writer.writerow(["Total Links", Link.objects.count()])
    writer.writerow(["Generated At", timezone.now().strftime("%Y-%m-%d %H:%M:%S")])
    writer.writerow([])

    # ============ USERS ============
    writer.writerow(["===== Users ====="])
    writer.writerow(["Model", "Username", "Email", "Joined", "Active", "Role"])
    for user in User.objects.all():
        role = (
            "Recruiter"
            if Job.objects.filter(recruiter=user).exists()
            else "JobSeeker"
            if hasattr(user, "jobseekerprofile")
            else "Admin/Other"
        )
        writer.writerow([
            "User",
            user.username,
            user.email,
            user.date_joined,
            user.is_active,
            role,
        ])
    writer.writerow([])

    # ============ JOB SEEKER PROFILES ============
    writer.writerow(["===== Job Seeker Profiles ====="])
    writer.writerow([
        "Model", "User", "Headline", "Education", "Location",
        "Projects", "Work Experience", "Skills", "Privacy"
    ])
    for seeker in JobSeekerProfile.objects.select_related("user"):
        writer.writerow([
            "JobSeekerProfile",
            seeker.user.username,
            seeker.headline or "",
            seeker.education or "",
            seeker.location or "",
            (seeker.projects or "").replace("\n", " "),
            (seeker.work_experience or "").replace("\n", " "),
            (seeker.skills or "").replace("\n", " "),
            seeker.privacy or "",
        ])
    writer.writerow([])

    # ============ LINKS ============
    writer.writerow(["===== Job Seeker Links ====="])
    writer.writerow(["Model", "User", "URL"])
    for link in Link.objects.select_related("profile__user"):
        writer.writerow([
            "Link",
            link.profile.user.username,
            link.url,
        ])
    writer.writerow([])

    # ============ JOBS ============
    writer.writerow(["===== Jobs ====="])
    writer.writerow(["Model", "Title", "Recruiter", "Location", "Created At", "Description"])
    for job in Job.objects.select_related("recruiter"):
        writer.writerow([
            "Job",
            job.title,
            job.recruiter.username if job.recruiter else "",
            getattr(job, "location", ""),
            job.created_at,
            (job.description or "").replace("\n", " "),
        ])
    writer.writerow([])
    
    return response


def get_admin_urls(urls):
    """Hook our export view into the default admin site."""
    def new_urls():
        my_urls = [
            path("export/all-data/", admin.site.admin_view(export_all_data)),
        ]
        return my_urls + urls
    return new_urls


# Extend the default admin.site
admin.site.get_urls = get_admin_urls(admin.site.get_urls())
