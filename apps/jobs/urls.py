from django.urls import path
from .views import JobListView,JobDetailView,JobMatchView,JobRecomendationView

urlpatterns=[
    path('',JobListView.as_view(),name='jobs'),
    path('<int:job_id>/match/<int:resume_id>',JobMatchView.as_view(),name='match job by resume'),
    path('<int:pk>/',JobDetailView.as_view(),name='jobs'),
    path('recommendations/<int:resume_id>/',JobRecomendationView.as_view(),name='jobs'),
]
