from django.urls import path

from .views import (
    DocumentUploadView,
    MyDocumentsView,
    RegisterView,
    DashboardView,
    ResumeSearchView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('upload/', DocumentUploadView.as_view()),
    path('my-documents/', MyDocumentsView.as_view()),
    path('dashboard/', DashboardView.as_view()),
    path('search/', ResumeSearchView.as_view()),
]