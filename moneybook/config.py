import os

# 프로젝트 루트 경로
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# 데이터 파일명 헤더
DATA_FILE_NAME_HEADER = os.getenv("DATA_FILE_NAME_HEADER", "dummy_data")
