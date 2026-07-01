
from django.db import models
from django.conf import settings

# Create your models here.
class Resume(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    file=models.FileField(upload_to='resumes/files')
    extracted_text=models.TextField(blank=True,default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


  
class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(
        Resume,
        on_delete=models.CASCADE,
        related_name='resume'
    )

    primary_role = models.CharField(
    max_length=100,
    null=True,
    blank=True
)

    secondary_roles = models.JSONField(default=list)

    technologies = models.JSONField(default=list)

    experience = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    score = models.IntegerField(null=True,
        blank=True)

    found_skills = models.JSONField(default=list)

    missing_skills = models.JSONField(default=list)

    strengths = models.JSONField(default=list)

    weaknesses = models.JSONField(default=list)

    suggestions = models.JSONField(default=list)

    summary = models.TextField(default='')
    created_at=models.DateTimeField(auto_now_add=True)