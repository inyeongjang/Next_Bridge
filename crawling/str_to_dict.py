import pandas as pd

# Excel 파일 읽기

file_path = r'C:\Users\jpk66\Desktop\nextbridge_iy\nextbridge\jobs\job_info.xlsx'  # 파일 경로를 지정하세요.
data = pd.read_excel(file_path)

def str_to_dict(str_conditions):
    # 문자열 내 불필요한 '{', '}', "'" 제거
    str_conditions = str_conditions.replace("{", "").replace("}", "").replace("'", "")
    
    # 문자열을 ,로 분리
    items = str_conditions.split(',')
    
    # 분리된 항목들을 key: value로 나누어 딕셔너리로 반환
    conditions_dict = {}
    for item in items:
        # 각 항목을 :를 기준으로 나누어 key와 value 추출
        key_value = item.split(':')
        if len(key_value) == 2:  # key와 value가 정상적으로 분리된 경우
            key = key_value[0].strip()  # 공백 제거
            value = key_value[1].strip()  # 공백 제거
            conditions_dict[key] = value
    
    return conditions_dict

# 각 열에 대해 str_to_dict 함수 적용
data['모집 조건'] = data['모집 조건'].apply(str_to_dict)
data['근무 조건'] = data['근무 조건'].apply(str_to_dict)
data['복리 후생'] = data['복리 후생'].apply(str_to_dict)

# 결과를 새로운 Excel 파일로 저장
output_file_path = r'C:\Users\jpk66\Desktop\nextbridge_iy\nextbridge\jobs\job_info3.xlsx'  # 결과 파일 경로를 지정하세요.

data.to_excel(output_file_path, index=False)

print("필터링된 데이터를 저장했습니다:", output_file_path)
