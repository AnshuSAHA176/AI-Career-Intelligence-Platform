from rest_framework import generics,filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from rest_framework.views import APIView
from .serializers import JobListSerializer,JobDetailsSerializer,JobRecommendationsSerializer
from rest_framework.response import Response
from ..resumes.models import ResumeAnalysis
from ..resumes.road_mape import match_resume,level_cheaker
from django.shortcuts import get_object_or_404
class JobListView(generics.ListAPIView):
    queryset=Job.objects.all()
    serializer_class=JobListSerializer
    filter_backends=[
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "title",
        "company",
        "primary_role",
        "technologies",
    ]

    filterset_fields = [
        "primary_role",
        "work_type",
        "employment_type",
    ]
    ordering_fields = ['posted_date' , 'company']


class JobDetailView(generics.RetrieveAPIView):
    queryset=Job.objects.all()
    serializer_class=JobDetailsSerializer

class JobMatchView(APIView):
    def post(self,request,job_id,resume_id):
        job=Job.objects.get(id=job_id)
        resume=ResumeAnalysis.objects.get(resume_id=resume_id,resume__user=request.user)
        result=match_resume(job.required_skills,resume.found_skills)
        return Response(result)
class JobRecomendationView(APIView):
    def post(self,request,resume_id):
        resume=get_object_or_404(
            ResumeAnalysis,
            resume_id=resume_id,
            resume__user=request.user,

        )
        jobs=Job.objects.filter(primary_role=resume.primary_role)
        serializer=JobRecommendationsSerializer(jobs,many=True)
        recommendations=serializer.data
        

        return Response(recommendations)


