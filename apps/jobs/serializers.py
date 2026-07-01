from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
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