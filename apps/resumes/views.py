from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .analyze import analyze_resume,analyze_resume_ai
from .models import Resume,ResumeAnalysis
from .serializers import ResumesListSerializer,ResumeSerializer,ResumeAnalysisSerializer,RoadMapSerializer,ReportSerializer,JobRole
from .utils import extract_text_from_pdf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .road_mape import road_map,match_resume
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ResumesView(generics.ListAPIView):
     
     serializer_class=ResumesListSerializer
     permission_classes=[IsAuthenticated]
     def get_queryset(self):
          return Resume.objects.filter(
               user=self.request.user,
               
        )
     


# For one resume----------------------------
class ResumeView(generics.RetrieveAPIView):
     
     serializer_class=ResumeSerializer
     permission_classes=[IsAuthenticated]
     def get_queryset(self):
          return Resume.objects.filter(
               user=self.request.user,
               
          )

# deleter resume
class ResumeDeleteView(generics.DestroyAPIView):
     serializer_class=ResumeSerializer
     permission_classes=[IsAuthenticated]
     def get_queryset(self):
          return Resume.objects.filter(
               user=self.request.user,
          )



class ResumeUploadView(generics.CreateAPIView):
    queryset=Resume.objects.all()
    serializer_class=ResumeSerializer
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser,FormParser]
    def perform_create(self, serializer):
            resume=serializer.save(user=self.request.user)
            text=extract_text_from_pdf(resume.file)
            resume.extracted_text=text
            resume.save(update_fields=["extracted_text"])


class ResumeAnalyzeView(APIView):

    def post(self, request):
        try:
               resume = Resume.objects.get(
                    user=request.user.id,
                    is_active=True
               )
        except Resume.DoesNotExist:
               raise NotFound("No active resume found. Please activate a resume first.")

        result = analyze_resume_ai(
            text=resume.extracted_text,
            target_role=request.user.profile.target_role
        )

        analysis, created = ResumeAnalysis.objects.update_or_create(
            resume=resume,
            defaults={
                "score": result.get("score", 0),
                "found_skills": result.get("found_skills", []),
                "missing_skills": result.get("missing_skills", []),
                "strengths": result.get("strengths", []),
                "weaknesses": result.get("weaknesses", []),
                "suggestions": result.get("suggestions", []),
                "summary": result.get("summary", ""),
                "primary_role": result.get("primary_role", ""),
                "secondary_roles": result.get("secondary_roles", []),
                "technologies": result.get("technologies", []),
                "experience": result.get("experience", {}).get("years"),
            }
        )

        serializer = ResumeAnalysisSerializer(analysis)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class RoadMapView(APIView):
     def post(self,request):
          resume= ResumeAnalysis.objects.get(
               
          )
          result=road_map(resume.missing_skills)
          serializer=RoadMapSerializer(result,many=True)
          return Response(serializer.data)


class ReportView(APIView):
     def get(self,request):
          try:
               resume=ResumeAnalysis.objects.get(resume__user=request.user ,resume__is_active=True)
          except ResumeAnalysis.DoesNotExist:
               raise NotFound("No active resume found. Please activate a resume first.")
          
          serializer=ReportSerializer(resume)
          data=serializer.data
          data['roadmap']=road_map(resume.missing_skills)
          return Response(data)

class job_match(APIView):
     def post(self,request):
          try:
               resume=ResumeAnalysis.objects.get(resume__user=request.user ,resume__is_active=True)
          except ResumeAnalysis.DoesNotExist:
               raise NotFound("No active resume found. Please activate a resume first.")
          serializer=JobRole(data=request.data)
          serializer.is_valid(raise_exception=True)
          job_role = serializer.validated_data[
    "job_role"
]
          result=match_resume(job_role,resume.found_skills)
          return Response(result)
     


class ResumeActiveView(APIView):
     permission_classes= [IsAuthenticated]
     def patch(self,request,resume_id):
          Resume.objects.filter(user=request.user).update(is_active=False)
          resume=get_object_or_404(
               Resume,
               id=resume_id,
               user=request.user,
          )
          resume.is_active=True
          resume.save(update_fields=['is_active'])
          return Response({
                 "message": "Resume activated successfully."
          })