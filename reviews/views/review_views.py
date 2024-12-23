from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q

from jobs.models import JobPosting
from reviews.models import Review
from reviews.forms import ReviewForm


# 리뷰 등록(리뷰 저장)
@login_required(login_url='common:login')
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():               # 폼이 유효하다면
            # 입력된 회사 이름으로 JobPosting 검색
            company_name = form.cleaned_data['company_name']
            try:
                # 대소문자 무시 및 유사 검색 적용
                company = JobPosting.objects.get(company_name__iexact=company_name)
            except JobPosting.DoesNotExist:
                form.add_error('company_name', '해당 회사가 존재하지 않습니다.')
                return render(request, 'reviews/review_form.html', {'form': form})

            # 리뷰 생성 및 저장
            review = form.save(commit=False)
            review.company = company
            review.author = request.user  # 로그인된 사용자로 설정
            review.create_date = timezone.now()
            review.save()
            return redirect('reviews:review_list')  # 리뷰 목록으로 이동

    else:
        form = ReviewForm()

    return render(request, 'reviews/review_form.html', {'form': form})

# 리뷰 수정
@login_required(login_url='common:login')
def review_modify(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('reviews:review_detail', review_id=review.id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.modify_date = timezone.now()  # 수정일시 저장
            review.save()
            return redirect('reviews:review_detail', review_id=review.id)
    else:
        form = ReviewForm(instance=review)
    context = {'form': form}
    return render(request, 'reviews/review_form.html', context)

# 리뷰 삭제
@login_required(login_url='common:login')
def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('reviews:review_detail', review_id=review.id)
    review.delete()
    return redirect('reviews:review_list')


# 리뷰 추천
@login_required(login_url='common:login')
def review_vote(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        review.voter.add(request.user)
    return redirect('reviews:review_detail', review_id=review.id)