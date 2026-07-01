from django.db import models


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



    def __str__(self):
        return self.title