from rest_framework import generics,filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job,SaveJobs,ApplicationStatusHistory
from rest_framework.views import APIView
from .serializers import JobListSerializer,JobDetailsSerializer,JobRecommendationsSerializer,SaveJobSerializer,StatusSerializer,TimelineSerializer
from rest_framework.response import Response
from ..resumes.models import ResumeAnalysis
from ..resumes.road_mape import match_resume,level_cheaker
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class JobListView(generics.ListAPIView):
    queryset=Job.objects.all()
    serializer_class=JobListSerializer
    filter_backends=[
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    ordering=['-posted_date']

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




# save jobs get save jobs delete save jobs:-

class SaveJobsView(APIView):
    def post(self,request,job_id):
        job=get_object_or_404(Job,id=job_id)
        save_job,create=SaveJobs.objects.get_or_create(
            user=request.user,
            job=job
            
            )
        if create:
            ApplicationStatusHistory.objects.create(
                save_job=save_job,
                status=SaveJobs.Status.SAVED
            )
        
        
        return Response ({ "message": "Job saved successfully."},
                         status=status.HTTP_201_CREATED,)
    
class DeleteSaveJobView(APIView):
    def delete(self,request,job_id):
        SaveJobs.objects.filter(
            user=request.user,
            job_id=job_id,
        ).delete()
        return Response({"message": "Job removed from saved jobs."},  status=status.HTTP_200_OK,)
    
class GetSaveJobView(generics.ListAPIView):
    
    serializer_class=SaveJobSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return SaveJobs.objects.filter(
            user=self.request.user,
            
        )
    

# status

class StatusView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request,job_id):
        serializer=StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        savejob=get_object_or_404(
            SaveJobs,
            user=request.user,
            job_id=job_id,
        )
        status=serializer.validated_data['status']
        if not status:
            return Response(
                {"error": "Status is required."},
                status=400)
        
        savejob.status=status
        savejob.save(update_fields=['status'])
        ApplicationStatusHistory.objects.create(
            save_job=savejob,
            status=status
        )
        return Response({
            "message": "Status updated successfully."
        })
    

class ApplicationTimelineView(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=TimelineSerializer
    def get_queryset(self):
        return ApplicationStatusHistory.objects.filter(
            save_job__user=self.request.user,
            save_job__job_id=self.kwargs['job_id'],
            
                    )
    
