from django.db import models

class JobPosting(models.Model):
    company_name = models.CharField(max_length=255)         # 회사 이름
    title = models.CharField(max_length=255)                # 공고 제목
    upper_region = models.CharField(max_length=255)         # 지역 대분류
    lower_region = models.CharField(max_length=255)         # 지역 대분류
    salary = models.CharField(max_length=255)               # 급여
    upper_field = models.CharField(max_length=255)          # 직무 분야
    lower_field = models.CharField(max_length=255)          # 직무 세부
    post_date = models.DateField()                          # 등록 날짜
    due_date = models.DateField()                           # 채용 마감일
    description = models.TextField()                        # 상세 근무 요강

    ### 추가
    company_address = models.CharField(max_length=255, default="Unknown")  # 회사 주소
    recruit_conditions = models.JSONField(null=True, blank=True)  # 모집 조건
    work_conditions = models.JSONField(null=True, blank=True)  # 근무 조건
    welfare_conditions = models.JSONField(null=True, blank=True)  # 복리후생

    def __str__(self):
        return self.company_name

class Resume(models.Model):
    job = models.ForeignKey('JobPosting', on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job.title} - {self.file.name}"