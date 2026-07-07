from django.db import models
from config import settings

class Job(models.Model):

    title = models.CharField(max_length=255)

    company = models.CharField(max_length=255)

    location = models.CharField(max_length=255)

    description = models.TextField()

    required_skills = models.JSONField(default=list)

    category = models.CharField(
        max_length=100,
        blank=True
    )

    posted_date = models.DateField(
        null=True,
        blank=True
    )

    source = models.CharField(max_length=100)

    url = models.URLField(unique=True)

    

    primary_role = models.CharField(max_length=100, blank=True, default="")

    secondary_roles = models.JSONField(default=list)

    seniority = models.CharField(max_length=30, blank=True, default="Unknown")

    work_type = models.CharField(max_length=30, blank=True, default="Unknown")

    employment_type = models.CharField(max_length=30, blank=True, default="Unknown")

    technologies = models.JSONField(default=list)

    minimum_experience = models.PositiveIntegerField(
    null=True,
    blank=True
)

    maximum_experience = models.PositiveIntegerField(
    null=True,
    blank=True
)

    ai_summary = models.TextField(
    blank=True,
    default=""
)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=["primary_role"]),
            models.Index(fields=["company"]),
            models.Index(fields=["work_type"]),
            models.Index(fields=["employment_type"]),
            models.Index(fields=["posted_date"]),
        ]


    def __str__(self):
        return self.title
    


class SaveJobs(models.Model):
    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    job=models.ForeignKey(Job,on_delete=models.CASCADE,name="job")
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.SAVED)
    saved_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=["user","job"],
                name="unique_save_job"
            )
        ]

class ApplicationStatusHistory(models.Model):
    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    save_job=models.ForeignKey(SaveJobs,on_delete=models.CASCADE, related_name="timeline")
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.SAVED)
    notes = models.TextField(
    blank=True,
    default="")

    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']

