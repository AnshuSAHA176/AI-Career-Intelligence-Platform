from django.shortcuts import render
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import RegisterSerializer,LoginSerializer,UserProfileSerializer,ProfileSerializer,DashboardSerializer
from .models import User,Profile
from apps.resumes.models import ResumeAnalysis
from apps.jobs.models import ApplicationStatusHistory,SaveJobs,Job

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        return Response({
                    "access": str(access),
                    "refresh": str(refresh)
                },status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=self.request.user
        serializer=UserProfileSerializer(user)
        return Response(serializer.data)
    def put(self,request):
        profile=request.user.profile
        serializer=ProfileSerializer(profile,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DashboardView(APIView):
    permission_classes=[IsAuthenticated]
    @method_decorator(cache_page(60*15))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request):
        profile, _ = Profile.objects.get_or_create(
    user=request.user
)
        resume = get_object_or_404(
                ResumeAnalysis,
                resume__user=request.user,
                resume__is_active=True,
            )
        saved=SaveJobs.objects.filter(
            user=request.user,
            status=SaveJobs.Status.SAVED
        ).count()
        applied=SaveJobs.objects.filter(
            user=request.user,
            status=SaveJobs.Status.APPLIED
        ).count()
        interview=SaveJobs.objects.filter(
            user=request.user,
            status=SaveJobs.Status.INTERVIEW
        ).count()
        offer=SaveJobs.objects.filter(
            user=request.user,
            status=SaveJobs.Status.OFFER
        ).count()
        accepted=SaveJobs.objects.filter(
            user=request.user,
            status=SaveJobs.Status.ACCEPTED
        ).count()
        rejected=SaveJobs.objects.filter(
            user=request.user,
            status=SaveJobs.Status.REJECTED
        ).count()
        withdrawn=SaveJobs.objects.filter(
            user=request.user,
            status=SaveJobs.Status.WITHDRAWN
        ).count()
        job_statistics = {
        "saved": saved,
        "applied": applied,
        "interview": interview,
        "offer": offer,
        "accepted": accepted,
        "rejected": rejected,
        "withdrawn": withdrawn,
    }
        recommended_jobs=Job.objects.filter(
            primary_role=resume.primary_role,
        ).count()
        recent_activity=ApplicationStatusHistory.objects.filter(
            save_job__user=request.user
        ).select_related("save_job__job").order_by("-created_at")[:5]
        activities =[]
        for activity in recent_activity:
            activities.append({
                "job":activity.save_job.job.title,
                "status":activity.status,
                "created_at":activity.created_at,
            })

        data = {
            "user": {
                "name": request.user.get_full_name() or request.user.username,
                "target_role": profile.target_role
                ,
            },

            "resume": {
                "title": resume.resume.title,
                "score": resume.score,
                "primary_role": resume.primary_role,
                "uploaded_at": resume.resume.uploaded_at,
            },

            "job_statistics": job_statistics,

            "skills": {
                "found": len(resume.found_skills),
                "missing": len(resume.missing_skills),
            },

            "recommended_jobs": recommended_jobs,

            "recent_activity": activities,
        }
        serializer = DashboardSerializer(instance=data)

        return Response(serializer.data)