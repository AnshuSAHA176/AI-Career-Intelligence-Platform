from django.urls import path
from .views import ResumeDeleteView,ResumeUploadView,ResumeAnalyzeView,RoadMapView,ReportView,job_match,ResumesView,ResumeView
urlpatterns=[
    path('',ResumesView.as_view(),name='list of resumes'),
    path('<int:pk>/',ResumeView.as_view(),name='for one resume'),
    path('<int:pk>/delete/',ResumeDeleteView.as_view(),name='delete resume'),
    path('upload/',ResumeUploadView.as_view(),name='upload'),
    path("<int:resume_id>/analyze/",ResumeAnalyzeView.as_view(),name='analyzed_resume'),
    path("<int:resume_id>/roadmap/",RoadMapView.as_view(),name='analyzed_resume'),
    path("<int:resume_id>/report/",ReportView.as_view(),name='report_resume'),
    path("<int:resume_id>/job-match/",job_match.as_view(),name='job_match'),
]
