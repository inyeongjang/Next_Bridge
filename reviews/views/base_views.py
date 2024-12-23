from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count, Avg

from reviews.models import Review
from jobs.models import JobPosting

def index(request):
    # 검색어가 있을 경우 해당 회사들 가져오기
    rw = request.GET.get('rw','') # 검색어가 있으면 rw에 저장
    company_list = JobPosting.objects.all()
    if rw:
        company_list = JobPosting.objects.filter(
            Q(company_name__icontains=rw)
        )

        # 검색된 회사들에 대해서도 리뷰 개수와 평균 평점 계산
        company_list = company_list.annotate(
            review_count=Count('company_reviews'),  # 리뷰 개수 계산
            average_rating=Avg('company_reviews__rating')  # 평균 평점 계산
        )
    else:
        # 리뷰가 많은 순으로 9개 회사 가져오기
        company_list = JobPosting.objects.annotate(
            review_count=Count('company_reviews'),  # 리뷰 개수 계산
            average_rating=Avg('company_reviews__rating')  # 평균 평점 계산
        ).order_by('-review_count')[:9]  # 리뷰 개수가 많은 순으로 정렬

    # 최신 3개의 리뷰를 가져옵니다.
    latest_reviews = Review.objects.order_by('-create_date')[:3]

    context = {
        'latest_reviews': latest_reviews, # 최신 리뷰
        'companies': company_list, # 검색된 회사들
        'range': range(1, 6),
        'rw': rw,
    }
    # 최신 리뷰를 템플릿으로 전달
    return render(request, 'reviews/review_main.html', context)

def review_list(request):
    review_list = Review.objects.order_by('-create_date')
    context = {
        'review_list': review_list,
        'range': range(1, 6),  # 1부터 5까지 반복
    }
    return render(request, 'reviews/review_list.html', context)


# 리뷰 상세보기
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    context = {
        'review': review,
        'range': range(1, 6),  # 1부터 5까지 반복
    }
    return render(request, 'reviews/review_detail.html', context)


# 회사 별 리뷰보기
def company_reviews(request, company_id):
    # 회사 정보 가져오기
    company = get_object_or_404(JobPosting, pk=company_id)

    # 해당 회사의 리뷰 필터링
    kw = request.GET.get('kw', '')   # 검색어
    # 해당 회사에 대한 리뷰 조회
    company_review_list = Review.objects.filter(company=company).order_by('-create_date')

    # 해당 회사의 채용공고 조회
    jobs = JobPosting.objects.filter(company_name=company.company_name)

    if kw:
        company_review_list = company_review_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(comment__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw)   # 질문 글쓴이 검색
        ).distinct()

    context = {
        'company' : company,
        'reviews' : company_review_list,
        'kw' : kw,
        'jobs': jobs
    }
    return render(request, 'reviews/company_reviews.html', context)


# (리뷰 입력에서) 회사 검색
def company_autocomplete(request):
    query = request.GET.get('query', '').strip()
    if query:
        companies = JobPosting.objects.filter(company_name__icontains=query)[:10]
        data = {'companies': [{'company_name': company.company_name} for company in companies]}
    else:
        data = {'companies': []}
    return JsonResponse(data)


# (메인페이지에서) 회사 검색
def company_search(request):
    query = request.GET.get('q', '')
    if query:
        companies = JobPosting.objects.filter(name__icontains=query)[:10]  # 최대 10개
        results = [{'id': company.id, 'name': company.name} for company in companies]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

