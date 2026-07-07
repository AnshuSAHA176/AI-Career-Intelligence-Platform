from django.urls import path
from .views import JobListView,JobDetailView,JobMatchView,JobRecomendationView,SaveJobsView,GetSaveJobView,DeleteSaveJobView,StatusView,ApplicationTimelineView

urlpatterns=[
    path('',JobListView.as_view(),name='jobs'),
    path('<int:job_id>/match/<int:resume_id>/',JobMatchView.as_view(),name='match job by resume'),
    path('<int:pk>/',JobDetailView.as_view(),name='jobs'),
    path('recommendations/<int:resume_id>/',JobRecomendationView.as_view(),name='jobs'),
    path('<int:job_id>/save/',SaveJobsView.as_view(),name='save_jobs'),
    path('saved/',GetSaveJobView.as_view(),name='get_jobs'),
    path('<int:job_id>/save/delete/',DeleteSaveJobView.as_view(),name='delete_jobs'),
    path('<int:job_id>/status/',StatusView.as_view(),name='status_update'),
    path('<int:job_id>/timeline/',ApplicationTimelineView.as_view(),name='status_update'),
]
