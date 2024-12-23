import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# 페이지를 위해 추가한 빼기 필터
@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def div(value, reg):
    return value // reg

# 마크다운으로 작성한 문서를 HTML 문서로 변환하는 필터
@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]   # nl2br: 줄바꿈 문자를 <br>로 바꿔줌, fenced_code: 마크다운의 소스코드 표현
    return mark_safe(markdown.markdown(value, extensions=extensions))

@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))