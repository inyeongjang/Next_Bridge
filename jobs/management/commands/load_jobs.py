import os
import pandas as pd
from django.core.management.base import BaseCommand
from jobs.models import JobPosting

class Command(BaseCommand):
    help = 'Load job postings from an Excel file into the database'

    def handle(self, *args, **kwargs):
        # Excel 파일 경로
        excel_file = os.path.join(os.path.dirname(__file__), 'job_info.xlsx')

        # 데이터 로드 및 유효성 검사
        self.stdout.write('Loading data from Excel...')
        df = pd.read_excel(excel_file)

        required_columns = ['회사 이름', '제목', '도/특별시/광역시', '시/군/구', '급여', '직무 분야', '세부 직무', '등록 날짜', '채용 마감일',
                            '상세 근무 요강', '주소', '모집 조건', '근무 조건', '복리 후생']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("엑셀 파일에 필요한 열이 누락되었습니다.")

        # 기존 데이터 삭제 및 새 데이터 저장
        JobPosting.objects.all().delete()
        for _, row in df.iterrows():
            JobPosting.objects.create(
                company_name=row['회사 이름'],
                title=row['제목'],
                upper_region=row['도/특별시/광역시'],
                lower_region=row['시/군/구'],
                salary=row['급여'],
                upper_field=row['직무 분야'],
                lower_field=row['세부 직무'],
                post_date=row['등록 날짜'],
                due_date=row['채용 마감일'],
                description=row['상세 근무 요강'],
                company_address=row['주소'],
                recruit_conditions=row['모집 조건'],
                work_conditions=row['근무 조건'],
                welfare_conditions=row['복리 후생']
            )

        self.stdout.write('Data successfully loaded into the database.')
