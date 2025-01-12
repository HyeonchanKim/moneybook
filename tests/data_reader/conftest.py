import os
import shutil
import uuid

import pandas as pd
import pytest

from moneybook.data_reader import data_reader
from moneybook.data_reader.data_reader import MONEYBOOK_FILE_SKIP_ROWS, MONEYBOOK_FILE_SKIP_FOOTER


@pytest.fixture(scope="function")
def base_tmp_path(monkeypatch):
    # 테스트용 데이터를 저장할 임시 경로.
    tmp_path = f"/tmp/{uuid.uuid4()}"
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)

    # 테스트를 위하여 데이터 파일의 경로를 monkey patch함.
    origin_data_dir = data_reader.DATA_DIR
    monkeypatch.setattr(data_reader, "DATA_DIR", tmp_path)

    yield tmp_path

    # 테스트로 임시로 설정한 몽키 패치와 테스트 경로 삭제.
    monkeypatch.setattr(data_reader, "DATA_DIR", origin_data_dir)
    shutil.rmtree(tmp_path)


@pytest.fixture(scope="function")
def base_excel_file(base_tmp_path):
    # 테스트로 사용할 데이터 파일. 상위 5줄, 하위 4줄에 불필요한 데이터를 포함하는 형태로 생성.
    data_1 = (
        [["."] * 10 for _ in range(MONEYBOOK_FILE_SKIP_ROWS)]
        + [
            ["날짜", "사용처", "사용내역", "현금", "카드", "출금통장", "카드분류", "분류", "태그", "낭비"],
            ["2023년12월31일", "CU", "장보기", "10000", "0", "", "", "저축/보험>예금", "", ""],
            ["2023년12월31일", "이마트", "편의점 간식", "0", "24000", "", "삼성카드", "교육/육아>학원/교재비", "", ""],
            ["2023년12월31일", "CU", "편의점 간식", "5000", "0", "", "", "의복/미용>헤어/뷰티", "", ""],
        ]
        + [["."] * 10 for _ in range(MONEYBOOK_FILE_SKIP_FOOTER)]
    )
    data_2 = (
        [["."] * 10 for _ in range(MONEYBOOK_FILE_SKIP_ROWS)]
        + [
            ["날짜", "사용처", "사용내역", "현금", "카드", "출금통장", "카드분류", "분류", "태그", "낭비"],
            ["2024년01월31일", "이마트", "외식", "0", "5000", "", "", "건강/문화>온라인", "", ""],
            ["2024년01월31일", "스타벅스", "커피", "10000", "0", "", "국민카드", "교통/차량>대중교통비", "", ""],
        ]
        + [["."] * 10 for _ in range(MONEYBOOK_FILE_SKIP_FOOTER)]
    )

    # pandas로 xls 파일 생성
    data_file_1 = base_tmp_path + "/dummy_data_1.xls"
    data_file_2 = base_tmp_path + "/dummy_data_2.xls"
    pd.DataFrame(data_1).to_excel(data_file_1, index=False, header=False, engine="openpyxl")
    pd.DataFrame(data_2).to_excel(data_file_2, index=False, header=False, engine="openpyxl")
