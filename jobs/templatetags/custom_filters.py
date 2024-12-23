# jobs/templatetags/custom_filters.py
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display_recruit_conditions(value):
    """
    문자열의 양 끝에 있는 중괄호({})를 제거하고,
    쉼표(,)로 구분된 값들이 같은 줄에 출력되도록 변환하며,
    HTML의 <ul>과 <li> 태그로 감싸서 출력합니다.
    """
    if not isinstance(value, str):
        return value

    # 양 끝의 중괄호 제거
    value = value.strip('{}')

    # 쉼표로 항목 분리
    items = value.split(', ')

    # 각 항목 처리
    formatted_items = []
    temp_key = None
    temp_value = []

    for item in items:
        # 키와 값을 ':' 기준으로 분리
        if ': ' in item:
            # 이전 항목 처리 (키-값 쌍 처리)
            if temp_key is not None and temp_value:
                formatted_items.append(f"<li>{temp_key} : {', '.join(temp_value)}</li>")
            
            # 새로운 키-값 처리
            key, val = item.split(': ', 1)
            # 작은따옴표 제거
            key = key.strip("'").strip()
            val = val.strip("'").strip()

            # 새로운 키-값을 처리하기 위한 초기화
            temp_key = key
            temp_value = [val]
        else:
            # 값만 있는 경우(쉼표 구분된 값들)
            temp_value.append(item.strip("'").strip())

    # 마지막 항목 처리 (for문 후 남은 값 처리)
    if temp_key is not None and temp_value:
        formatted_items.append(f"<li>{temp_key} : {', '.join(temp_value)}</li>")

    # <ul> 태그로 항목들을 감싸기
    html = f"<ul>{''.join(formatted_items)}</ul>"

    return mark_safe(html)
