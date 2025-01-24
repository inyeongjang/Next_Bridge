import pandas as pd
import os

# 엑셀 파일들이 있는 폴더 경로
folder_path = r'C:\Users\jpk66\Desktop\excel_files'

# 폴더 내의 모든 엑셀 파일을 읽어 리스트에 저장
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 빈 리스트 생성 (각 엑셀 파일에서 데이터를 읽은 후 리스트에 추가)
df_list = []

# 각 엑셀 파일을 읽어 DataFrame으로 변환하여 리스트에 추가
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)
    df_list.append(df)

# 모든 DataFrame을 하나로 합침 (세로 방향으로 합침)
merged_df = pd.concat(df_list, ignore_index=True)

# 합쳐진 데이터프레임을 새로운 엑셀 파일로 저장
merged_df.to_excel(r'C:\Users\jpk66\Desktop\merge.xlsx', index=False)
