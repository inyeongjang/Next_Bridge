from django.contrib import admin

from .models import JobPosting

class JobsAdmin(admin.ModelAdmin):
    search_fields = ['company_name'] # 제목으로 찾음

admin.site.register(JobPosting, JobsAdmin)