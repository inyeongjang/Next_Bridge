from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.models import User
from common.models import UserProfile

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    has_answer = models.BooleanField(default=True) # 답변가능 여부

    def __str__(self):
        return self.description if self.description else self.name  # description이 없으면 name 반환

    def get_absolute_url(self):
        return reverse('home:index', args=[self.name])


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')   # 글쓴이
    subject = models.CharField(max_length=200)                                                   # 제목
    content = models.TextField()                                                                 # 내용
    create_date = models.DateTimeField()                                                         # 등록 일시
    modify_date = models.DateTimeField(null=True, blank=True)                                    # 수정 일시
    voter = models.ManyToManyField(User, related_name='voter_question')                          # 추천인 추가
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question') # 카테고리

    def __str__(self):
        return self.subject

    @staticmethod
    def order_by_so(question_list, so):
        if so == 'recommend':
            # aggretation, annotation에는 relationship에 대한 역방향 참조도 가능 (ex. Count('voter'))
            question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        elif so == 'popular':
            question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
        else: # so == 'recent'
            question_list = question_list.order_by('-create_date')

        return question_list

    def get_absolute_url(self):
        return reverse('home:detail', args=[self.id])

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')     # 글쓴이
    question = models.ForeignKey(Question, on_delete=models.CASCADE)                             # 해당 질문
    content = models.TextField()                                                                 # 내용
    create_date = models.DateTimeField()                                                         # 등록 일시
    modify_date = models.DateTimeField(null=True, blank=True)                                    # 수정 일시
    voter = models.ManyToManyField(User, related_name='voter_answer')                            # 추천인 추가

    def __str__(self):
        return self.content

    @staticmethod
    def order_by_so(answer_list, so):
        # 정렬
        if so == 'recommend':
            # todonum_voter 필드 추가
            answer_list = answer_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        else:  # so == 'recent':
            answer_list = answer_list.order_by('-create_date')

        return answer_list

    def get_page(self, so='recommend'):
        answer_list = Answer.order_by_so(self.question.answer_set.all(), so)

        index = 0
        for _answer in answer_list:
            index += 1
            if self == _answer:
                break

        return (index - 1) // 5 + 1

    def get_absolute_url(self):
        return reverse('home:detail', args=[self.question.id]) + f'?page={self.get_page()}#answer_{self.id}'

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        if self.question:
            return reverse('home:detail', args=[self.question.id]) + '#comment_question_start'
        else:  # if self.answer:
            return reverse('home:detail', args=[self.answer.question.id]) + \
                   f'?page={self.answer.get_page()}#comment_{self.id}'
