from moneybook.data_reader.data_reader import read_moneybook_data


def test_data_reader(base_excel_file):
    result = read_moneybook_data()

    # 베이스로 만든 엑셀 파일에 포함되는 행의 개수만큼 데이터 프레임으로 생성되는지 테스트.
    assert len(result) == 5


def test_data_reader_empty(base_tmp_path):
    result = read_moneybook_data()

    # 엑셀 파일이 존재하지 않는 경우, 빈 DataFrame이 생성되는지 테스트.
    assert len(result) == 0
