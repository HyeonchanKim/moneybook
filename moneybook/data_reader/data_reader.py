import os

import pandas as pd

from moneybook.config import DATA_DIR, DATA_FILE_NAME_HEADER

MONEYBOOK_FILE_SKIP_ROWS = 4
MONEYBOOK_FILE_SKIP_FOOTER = 4


def read_moneybook_data() -> pd.DataFrame:
    moneybook_data = []

    # 파일을 월 순서대로 처리하기 위하여 정렬하여 처리
    for file_name in sorted(os.listdir(DATA_DIR)):
        # 더미 데이터/실제 데이터를 구분하여 사용하기 위하여 환경 변수로 선언한 헤더 이름으로 구분.
        if not file_name.startswith(DATA_FILE_NAME_HEADER):
            continue
        moneybook_data.append(
            pd.read_excel(
                os.path.join(DATA_DIR, file_name),
                skiprows=MONEYBOOK_FILE_SKIP_ROWS,
                skipfooter=MONEYBOOK_FILE_SKIP_FOOTER,
            )
        )

    return pd.concat(moneybook_data) if moneybook_data else pd.DataFrame()


if __name__ == '__main__':
    print(read_moneybook_data())
