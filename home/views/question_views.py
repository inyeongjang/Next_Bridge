from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question, Category

# 질문 등록(질문 저장)
@login_required(login_url='common:login')
def question_create(request, category_name):
    category = Category.objects.get(name=category_name)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():                         # 폼이 유효하다면
            question = form.save(commit=False)      # 임시 저장하여 question 객체를 리턴 받는다.
            question.author = request.user          # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()   # 실제 저장을 위해 작성일시를 설정한다.
            question.category = category
            question.save()                         # 데이터를 실제로 저장한다.
            return redirect(category)
    else:   # request.method == 'GET'
        form = QuestionForm()
    context = {'form': form, 'category': category}
    return render(request, 'home/question_form.html', context)

# 질문 수정
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('home:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('home:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'category': question.category}
    return render(request, 'home/question_form.html', context)

# 질문 삭제
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('home:detail', question_id=question.id)
    question.delete()
    return redirect(question.category)

