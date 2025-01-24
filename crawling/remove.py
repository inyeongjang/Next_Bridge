import pandas as pd

# Excel 파일 읽기

file_path = r'C:\Users\jpk66\Desktop\nextbridge_iy\nextbridge\jobs\job_info.xlsx'  # 파일 경로를 지정하세요.
data = pd.read_excel(file_path)

# 특정 조건을 만족하는 행을 삭제
regions_to_remove = ['서울특별시', '경기도', '인천광역시']
filtered_data = data[~data['도/특별시/광역시'].isin(regions_to_remove)]

# 결과를 새로운 Excel 파일로 저장
output_file_path = r'C:\Users\jpk66\Desktop\nextbridge_iy\nextbridge\jobs\job_info2.xlsx'  # 결과 파일 경로를 지정하세요.

filtered_data.to_excel(output_file_path, index=False)

print("필터링된 데이터를 저장했습니다:", output_file_path)
