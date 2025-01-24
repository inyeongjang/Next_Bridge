import pandas as pd
import re
from datetime import datetime

# 엑셀 파일 읽기
df = pd.read_excel(r'C:\Users\jpk66\Desktop\merge.xlsx')

# 1. 중복되는 행 제거
df = df.drop_duplicates()

# 2. Null 값이 있는 행 제거
df = df.dropna()

# 3. "급여" 열이 "원"으로 끝나지 않으면 제거
# "급여" 열을 문자열로 변환하고 "원"으로 끝나는지 확인
df = df[df['급여'].astype(str).str.endswith('원')]

# 4. "채용 마감일" 열이 ")"로 끝나지 않는 행 제거
# "채용 마감일" 열을 문자열로 변환하고 ")"로 끝나는지 확인
df = df[df['채용 마감일'].astype(str).str.endswith(')')]

# 5. 모집조건 열에서 '{'필'로 시작하는 값만 남기기
df = df[df['모집 조건'].apply(lambda x: isinstance(x, str) and x.startswith("{'필"))]

# 6. 근무조건 열에서 '{'고'로 시작하는 값만 남기기
df = df[df['근무 조건'].apply(lambda x: isinstance(x, str) and x.startswith("{'고"))]

# 7. 복리후생 열에서 '{'4'로 시작하는 값만 남기기
df = df[df['복리 후생'].apply(lambda x: isinstance(x, str) and x.startswith("{'4"))]

# 8. 딕셔너리가 비어있는 행 {} 제거
df = df[df['모집 조건'].apply(lambda x: x != '{}')]

# 9. '지역' 열을 공백 기준으로 '도/특별시/광역시'와 '시/군/구'로 나눔
df[['도/특별시/광역시', '시/군/구']] = df['지역'].str.split(' ', expand=True)
# 기존 '지역' 열 삭제
df.drop(columns=['지역'], inplace=True)

# 10. "직무" 열 분리
df[['직무 분야', '세부 직무']] = df['직무'].str.split(' > ', expand=True)
# 기존 '직무' 열 삭제
df.drop(columns=['직무'], inplace=True)

# 11. "등록 날짜" 변환
def convert_registration_date(date_str):
    try:
        # "등록 :" 제거 및 날짜 변환
        clean_date = re.sub(r'등록\s*[:：]\s*', '', date_str).strip()
        return pd.to_datetime(clean_date, format='%Y. %m. %d').strftime('%Y-%m-%d')
    except Exception as e:
        print(f"등록 날짜 변환 오류: {e}")
        return None

df['등록 날짜'] = df['등록 날짜'].apply(convert_registration_date)

# 12. "채용 마감일" 변환
def convert_deadline_date(date_str):
    try:
        # "채용마감 :" 제거, 괄호 안 내용 제거, 날짜 변환
        clean_date = re.sub(r'채용마감\s*[:：]\s*', '', date_str)
        clean_date = re.sub(r'\(.*\)', '', clean_date).strip()
        parts = clean_date.split('.')
        if len(parts[0].strip()) == 2:  # 연도가 2자리라면
            clean_date = f"20{parts[0].strip()}.{parts[1].strip()}.{parts[2].strip()}"
        return pd.to_datetime(clean_date, format='%Y.%m.%d').strftime('%Y-%m-%d')
    except Exception as e:
        print(f"채용 마감일 변환 오류: {e}")
        return None

df['채용 마감일'] = df['채용 마감일'].apply(convert_deadline_date)

df_reset = df.reset_index(drop=True)
# 결과 저장 (원하는 파일 이름으로 저장 가능)
df_reset.to_excel(r'C:\Users\jpk66\Desktop\new5_job_info.xlsx', index=False)