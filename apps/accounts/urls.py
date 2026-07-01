from django.urls import path
from .views import RegisterView,LoginView,ProfileView
urlpatterns=[
    path("register/",RegisterView.as_view(),name='registerview'),
    path("login/",LoginView.as_view(),name='loginview'),
    path("profile/",ProfileView.as_view(),name='profile')
]