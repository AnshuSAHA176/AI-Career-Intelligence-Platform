from django.urls import path
from .views import RegisterView,LoginView,ProfileView,DashboardView
urlpatterns=[
    path("register/",RegisterView.as_view(),name='registerview'),
    path("login/",LoginView.as_view(),name='loginview'),
    path("profile/",ProfileView.as_view(),name='profile'),
    path("dashboard/",DashboardView.as_view(),name='dashbord')
]