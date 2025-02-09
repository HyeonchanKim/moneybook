import os
from enum import StrEnum

# 프로젝트 루트 경로
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# 데이터 파일명 헤더
DATA_FILE_NAME_HEADER = os.getenv("DATA_FILE_NAME_HEADER", "dummy_data")


class Headers(StrEnum):
    DATE = "날짜"
    USAGE = "사용처"
    DETAILS = "사용내역"
    CASH = "현금"
    CARD = "카드"
    BANK = "출금통장"
    CARD_TYPE = "카드분류"
    CATEGORY = "분류"
    TAG = "태그"
    WASTE = "낭비"

    CATEGORY_L = "대분류"
    CATEGORY_S = "소분류"
