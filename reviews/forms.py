from django import forms
from .models import Review

# 리뷰 등록
class ReviewForm(forms.ModelForm):
    company_name = forms.CharField(
        label="회사 이름",
        widget=forms.TextInput(attrs={'placeholder': '회사 이름을 검색하세요'}),
        required=True,
    )

    class Meta:
        model = Review
        fields = ['subject', 'rating', 'comment']
        labels = {
            'subject' : '제목',
            'rating' : '별점',
            'comment' : '내용',
        }