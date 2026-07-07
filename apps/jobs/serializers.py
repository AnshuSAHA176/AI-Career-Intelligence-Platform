from rest_framework import serializers
from .models import Job,SaveJobs,ApplicationStatusHistory




class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields=[
            'id',
            'title','company',
            'location',
            'primary_role',
            'work_type',
            'employment_type',
            'minimum_experience',
            'technologies',
            'ai_summary'
        ]
class JobDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields="__all__"



class JobRecommendationsSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Job
        fields = [
            "job_id",
            "title",
            "company",
            "location",
            "primary_role",
            "work_type",
            "employment_type",
            "technologies",
            "ai_summary",
        ]

class SaveJobSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    class Meta:
        model=SaveJobs
        fields=[
            "job",
            'status',
            'saved_at',
        ]

class StatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=SaveJobs.Status.choices
    )


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApplicationStatusHistory
        fields=[
            'status',
            'notes',
            'created_at',
        ]
