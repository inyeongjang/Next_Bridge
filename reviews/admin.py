from django.contrib import admin
from .models import Review

# 리뷰(Review) 조회
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['subject'] # 제목으로 찾음

admin.site.register(Review, ReviewAdmin)
