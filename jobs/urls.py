# jobs/urls.py
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),  # '/' 경로로 job_list 뷰를 처리
    path('<int:job_id>/', views.job_detail, name='job_detail'),  # '/' 경로로 job_list 뷰를 처리
    path('<int:job_id>/upload_resume/', views.upload_resume, name='upload_resume'),
    path('company/<int:company_id>/reviews/', views.company_reviews, name='company_reviews'),
]