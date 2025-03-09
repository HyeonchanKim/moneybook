import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_tree_select import tree_select

# python 모듈 경로에 프로젝트 루트 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moneybook.config import Headers
from moneybook.data_reader.data_reader import read_moneybook_data


def main():
    setup_page()

    df = read_moneybook_data()
    preprocess_data(df)

    df = filter_data(df)

    st.write(df)
    show_spend_chart(df)
    show_cumulative_spend_chart(df)


def setup_page():
    """
    Streamlit 기본 페이지 설정.
    """
    st.set_page_config(layout="wide")
    st.title("가계부 대시보드")


def preprocess_data(df: pd.DataFrame):
    """
    데이터 시각화를 위해 데이터 전처리.
    """
    df[Headers.DATE] = pd.to_datetime(df[Headers.DATE], format="%Y년%m월%d일")
    df[Headers.SPENT] = df[Headers.CARD] + df[Headers.CASH]
    df[[Headers.CATEGORY_L, Headers.CATEGORY_S]] = df[Headers.CATEGORY].str.split(">", expand=True, n=1)


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    사이드바에서 필터링 옵션 관련 설정하고, 필터링을 진행.
    """
    st.sidebar.header("필터링 옵션")

    df = filter_by_date(df)

    return df


def filter_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    날짜 범위 필터링. 날짜에 포함되는 데이터만 사용함.
    """
    selected_date = st.sidebar.date_input(
        "날짜 범위",
        value=[df[Headers.DATE].min().date(), df[Headers.DATE].max().date()],
        min_value=df[Headers.DATE].min().date(),
        max_value=df[Headers.DATE].max().date(),
    )
    if isinstance(selected_date, tuple) and len(selected_date) == 2:
        start_date, end_date = selected_date
        df = df[(df[Headers.DATE] >= pd.to_datetime(start_date)) & (df[Headers.DATE] <= pd.to_datetime(end_date))]

    return df


def filter_by_detail(df: pd.DataFrame) -> pd.DataFrame:
    """
    사용내역 필터링. 사용내역이 포함되어있으면 제외함.
    """
    excluded_details = st.sidebar.multiselect("사용내역 제외", df[Headers.DETAILS].unique())
    if excluded_details:
        df = df[~df[Headers.DETAILS].isin(excluded_details)]

    return df


def filter_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    카테고리 필터링. 선택한 카테고리만 사용함.
    """
    st.sidebar.write("카테고리 포함")
    df[[Headers.CATEGORY_L, Headers.CATEGORY_S]] = df[Headers.CATEGORY].str.split(">", expand=True, n=1)
    tree_data = convert_df_to_tree_data(df)

    # `container()`를 사용해서 사이드바에서 실행
    with st.sidebar.container():
        selected = tree_select(tree_data)
    df = df[df[Headers.CATEGORY].isin(selected["checked"])]

    return df


def convert_df_to_tree_data(df: pd.DataFrame) -> list:
    """
    DataFrame으로부터 카테고리 트리 데이터를 생성.
    """
    tree = dict()

    for _, row in df.iterrows():
        category_l = row[Headers.CATEGORY_L]
        category_s = row[Headers.CATEGORY_S]

        if category_l not in tree:
            tree[category_l] = set()
        tree[category_l].add(category_s)

    tree_data = [
        {
            "label": category_l,
            "value": category_l,
            "children": [{"label": category_s, "value": f"{category_l}>{category_s}"} for category_s in categories_m],
        }
        for category_l, categories_m in tree.items()
    ]
    return tree_data


def show_spend_chart(df: pd.DataFrame):
    """
    날짜별 지출 금액을 일 단위로 확인할 수 있는 그래프 생성.
    """
    date_spend_df = df.groupby(Headers.DATE)[Headers.SPENT].sum().reset_index()
    date_spend_chart = px.bar(
        date_spend_df, x=Headers.DATE, y=Headers.SPENT, title="날짜별 지출 금액", labels={Headers.SPENT: "원", Headers.DATE: "날짜"}
    )
    st.plotly_chart(date_spend_chart, use_container_width=True)


def show_cumulative_spend_chart(df: pd.DataFrame):
    """
    날짜별 지출 금액을 누적으로 확인할 수 있는 그래프 생성.
    """
    date_cumulative_cash_df = df.groupby(Headers.DATE)[Headers.SPENT].sum().cumsum().reset_index()
    date_cash_cumulative_chart = px.line(
        date_cumulative_cash_df,
        x=Headers.DATE,
        y=Headers.SPENT,
        title="날짜별 지출 금액",
        labels={Headers.SPENT: "원", Headers.DATE: "날짜"},
    )
    st.plotly_chart(date_cash_cumulative_chart, use_container_width=True)


if __name__ == "__main__":
    main()
