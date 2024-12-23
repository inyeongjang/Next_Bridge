from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from common.forms import UserForm
from common.models import UserProfile

# 회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # 기본 User 모델에 사용자 저장
            user = form.save()
            #form.save()

            # UserProfile 모델에 추가 정보 저장
            country = form.cleaned_data.get('country') # 출신 국가 저장
            address = form.cleaned_data.get('address') # 현재 거주지 저장
            birth_date = form.cleaned_data.get('birth_date') # 생년월일

            UserProfile.objects.create(user=user, country=country, address=address, birth_date=birth_date)

            # 사용자 인증 후 로그인
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인

            return redirect('home:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('index')


