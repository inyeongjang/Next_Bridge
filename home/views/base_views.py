from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.shortcuts import render, get_object_or_404

from ..models import Question, Answer, Category
from jobs.models import JobPosting

# home 목록 출력
def index(request, category_name='community'):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent') # 정렬기준

    # 회사 정렬
    company_list = JobPosting.objects.all()

    category = get_object_or_404(Category, name=category_name)
    # 정렬
    question_list = Question.order_by_so(
        Question.objects.filter(category=category).select_related('author__profile'), so)

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    # 회사 평점 순으로 정렬
    company_list = JobPosting.objects.annotate(
        review_count=Count('company_reviews'),  # 리뷰 개수 계산
        average_rating=Avg('company_reviews__rating')  # 평균 평점 계산
    ).order_by('-average_rating')[:10]

    # 페이징 처리
    paginator = Paginator(question_list, 15) # 페이지 당 15개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'page': page,
        'kw': kw,
        'so': so,
        'category': category,
        'companies': company_list,
    }
    return render(request, 'home/question_list.html', context)

# 질문 상세
def detail(request, question_id):
    # 입력파라미터
    page = request.GET.get('page', '1')  # 페이지
    so = request.GET.get('so', 'recommend')  # 정렬기준
    question = get_object_or_404(Question, pk=question_id)

    answer_list = Answer.order_by_so(Answer.objects.filter(question=question), so)

    # 페이징 처리
    paginater = Paginator(answer_list, 5) # 페이지당 5개씩 보여주기
    page_obj = paginater.get_page(page)

    context = {'question': question, 'answer_set': page_obj, 'page': page, 'so': so, 'category': question.category}
    return render(request, 'home/question_detail.html', context)
