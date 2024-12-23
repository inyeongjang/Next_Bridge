from django import forms
from django_countries.fields import CountryField
import django.contrib.auth.forms as auth_forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(auth_forms.UserCreationForm):
    country = CountryField(blank_label='(선택하세요)').formfield()
    address = forms.CharField(max_length=255, required=True, label="현재 주소")
    birth_date = forms.DateField(
        required=True,
        label="생년월일",
        widget=forms.DateInput(attrs={'type': 'date'}) # HTML5 date picker
    )
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "country", "address", "birth_date")


# 프로필 수정 폼
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['country', 'address', 'birth_date']  # 수정하고자 하는 필드들

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # date input 위젯
        required=True
    )

