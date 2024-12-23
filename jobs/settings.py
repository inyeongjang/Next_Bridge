import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 세션 만료 기간 설정 (옵션)
SESSION_COOKIE_AGE = 86400  # 하루 (초 단위)
SESSION_SAVE_EVERY_REQUEST = True  # 모든 요청에서 세션 갱신