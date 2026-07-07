from rest_framework import serializers
from .models import Resume,ResumeAnalysis


class ResumesListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resume
        fields=[
            'id',
            'title',
            'file',
            'uploaded_at',
            'updated_at',
            'is_active',
        ]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resume
        fields = [
                "id",
                "title",
                "file",
                "extracted_text",
                "uploaded_at",
                "updated_at",
                "is_active",
            ]
        read_only_fields = [
                "id",
                "extracted_text",
                "uploaded_at",
                "updated_at",
            ]

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        resume=ResumeSerializer()
        model=ResumeAnalysis
        fields=[
            'id',
            'resume',
            'score',
            
            'found_skills',
            'missing_skills',
             'created_at',
             'strengths',
            'weaknesses',
            'suggestions',
            'summary',


        ]

class RoadMapSerializer(serializers.Serializer):
    skill=serializers.CharField()
    steps=serializers.ListField(
        child=serializers.CharField()
    )

class ReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ResumeAnalysis
        fields=['score','found_skills','missing_skills','strengths','weaknesses','suggestions','summary']
class JobRole(serializers.Serializer):
    job_role=serializers.CharField()
    

