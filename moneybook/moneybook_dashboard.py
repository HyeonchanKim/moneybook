import os
import sys

import streamlit as st

# python 모듈 경로에 프로젝트 루트 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moneybook.data_reader.data_reader import read_moneybook_data


def main():
    st.title("가계부 대시보드")

    df = read_moneybook_data()
    st.write(df)


if __name__ == "__main__":
    main()