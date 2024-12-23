from django.contrib import admin
from .models import Question, Answer, Category, Comment

# 질문(Question) 조회
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject'] # 제목으로 찾음

admin.site.register(Question, QuestionAdmin)

# 답변(Answer) 조회
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['content'] # 내용으로 찾음

admin.site.register(Answer, AnswerAdmin)

# 카테고리(Category) 조회
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

# 댓글(Comment) 조회
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Comment, CommentAdmin)


