import os
import pandas as pd
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import JobPosting
from reviews.models import Review

def job_list(request):

    # 검색 조건 가져오기
    upper_region = request.GET.get('upper_region', '').strip()  # 근무지
    lower_region = request.GET.get('lower_region', '').strip()  # 근무지
    upper_field = request.GET.get('upper_field', '').strip()  # 직무
    lower_field = request.GET.get('lower_field', '').strip()  # 세부 직무 
    query = request.GET.get('query', '').strip()  # 검색어

    # 필터링 로직
    jobs = JobPosting.objects.all()
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if upper_field:  # 대분류로 필터링
        jobs = jobs.filter(Q(upper_field=upper_field) | Q(lower_field=lower_field))  # 소분류도 포함
    if lower_field:  # 소분류로 필터링
        jobs = jobs.filter(lower_field=lower_field)
    if upper_region:  # 대분류로 필터링
        jobs = jobs.filter(Q(upper_region=upper_region) | Q(lower_region=lower_region))  # 소분류도 포함
    if lower_region:  # 소분류로 필터링
        jobs = jobs.filter(lower_region=lower_region)

    # 직무 계층 구조 생성 (가나다 순, 기타를 마지막으로)
    fields_hierarchy = {}
    fields = JobPosting.objects.values('upper_field', 'lower_field').distinct()
    for item in fields:
        fields_hierarchy.setdefault(item['upper_field'], []).append(item['lower_field'])

    fields_hierarchy = {
        key: sorted(values, key=lambda x: (x == '기타', x))  # "기타"를 마지막에 위치
        for key, values in sorted(fields_hierarchy.items(), key=lambda x: (x[0] == '기타', x[0]))
    }

    # 근무지 계층 구조 생성 (가나다 순, 기타를 마지막으로)
    regions_hierarchy = {}
    regions = JobPosting.objects.values('upper_region', 'lower_region').distinct()
    for item in regions:
        regions_hierarchy.setdefault(item['upper_region'], []).append(item['lower_region'])

    regions_hierarchy = {
        key: sorted(values, key=lambda x: (x == '기타', x))  # "기타"를 마지막에 위치
        for key, values in sorted(regions_hierarchy.items(), key=lambda x: (x[0] == '기타', x[0]))
    }

    # 페이지네이션 처리
    paginator = Paginator(jobs, 10)  # 한 페이지에 10개씩
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 템플릿에 전달할 데이터
    context = {
        'jobs': page_obj,
        'fields_hierarchy': fields_hierarchy,
        'regions_hierarchy': regions_hierarchy,
        'upper_field': upper_field,
        'lower_field': lower_field,
        'upper_region': upper_region,
        'lower_region': lower_region,
        'query': query,
    }

    return render(request, 'jobs/job_list.html', context)


def job_detail(request, job_id):
    job = JobPosting.objects.get(id=job_id)  # 주어진 id에 해당하는 Job 객체 가져오기
    return render(request, 'jobs/job_detail.html', {'job': job})  # job_detail 템플릿 렌더링


def upload_resume(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)

    # 업로드한 공고 ID를 세션에서 가져옴
    uploaded_jobs = request.session.get('uploaded_jobs', [])

    if job_id in uploaded_jobs:
        # 이미 업로드한 경우
        return JsonResponse({'message': '이미 이력서를 업로드한 공고입니다.', 'success': False})

    # 업로드 처리 로직 (여기서는 실제 저장하지 않음)
    uploaded_jobs.append(job_id)
    request.session['uploaded_jobs'] = uploaded_jobs  # 세션에 저장

    return JsonResponse({'message': '이력서가 성공적으로 업로드되었습니다.', 'success': True})


def company_reviews(request, company_id):
    company = get_object_or_404(JobPosting, id=company_id)

    # 해당 회사에 대한 리뷰 조회
    reviews = Review.objects.filter(company=company).order_by('-create_date')

    # 해당 회사의 채용 공고 조회
    jobs = JobPosting.objects.filter(company_name=company.company_name)

    context = {
        'company': company,
        'reviews': reviews,
        'jobs': jobs
    }

    return render(request, 'jobs/company_review.html', context)