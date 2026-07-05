from django.urls import path
from .views import ResumeDeleteView,ResumeUploadView,ResumeAnalyzeView,RoadMapView,ReportView,job_match,ResumesView,ResumeView,ResumeActiveView
urlpatterns=[
    path('',ResumesView.as_view(),name='list of resumes'),
    path('<int:pk>/',ResumeView.as_view(),name='for one resume'),
    path('<int:pk>/delete/',ResumeDeleteView.as_view(),name='delete resume'),
    path('upload/',ResumeUploadView.as_view(),name='upload'),
    path("analyze/",ResumeAnalyzeView.as_view(),name='analyzed_resume'),
    path("roadmap/",RoadMapView.as_view(),name='analyzed_resume'),
    path("report/",ReportView.as_view(),name='report_resume'),
    path("job-match/",job_match.as_view(),name='job_match'),
    path("<int:resume_id>/activate/",ResumeActiveView.as_view(),name='resume_actived'),
   
]
