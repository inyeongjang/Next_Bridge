from django.db import models
from jobs.models import JobPosting # jobs 앱의 모델을 가져오기
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from common.models import UserProfile

class Review(models.Model):
    company = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='company_reviews', null=False, blank=False ) # jobs의 JobPosting과 연결
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_reviews')
    subject = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(
        default=3,  # 기본값을 3으로 설정
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )  # 1~5점 평가
    comment = models.TextField()
    create_date = models.DateTimeField() # 등록 일시
    modify_date = models.DateTimeField(null=True, blank=True) # 수정 일시
    voter = models.ManyToManyField(User, related_name='voter_reviews') # 추천인 추가

    def __str__(self):
        return self.subject
